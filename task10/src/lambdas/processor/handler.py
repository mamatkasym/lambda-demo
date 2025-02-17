import json
import os
import uuid
from decimal import Decimal

import boto3
import requests
from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger(__name__)

from aws_xray_sdk.core import xray_recorder

patch(['boto3'])


class Processor(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass

    def handle_request(self, event, context):
        """
        Explain incoming event here
        """
        _LOG.info(f"EVENT: {event}")
        params = {
            "latitude": 52.54,
            "longitude": 13.41,
            "hourly": ["temperature_2m", "precipitation", "wind_speed_10m"],
            "current": ["temperature_2m", "relative_humidity_2m"]
        }

        response = requests.get(
            "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m")

        data = response.json()
        obj = {
            "id": uuid.uuid4().hex,
            "forecast": {
                "elevation": data["elevation"],
                "generationtime_ms": data["generationtime_ms"],
                "hourly": {
                    "temperature_2m": data["hourly"]["temperature_2m"],
                    "time": data["hourly"]["time"]
                },
                "hourly_units": {
                    "temperature_2m": data["hourly_units"]["temperature_2m"],
                    "time": data["hourly_units"]["time"]
                },
                "latitude": data["latitude"],
                "longitude": data["longitude"],
                "timezone": data["timezone"],
                "timezone_abbreviation": data["timezone_abbreviation"],
                "utc_offset_seconds": data["utc_offset_seconds"]
            }
        }
        obj = json.loads(json.dumps(obj), parse_float=Decimal)

        dynamodb = boto3.resource('dynamodb', region_name=os.environ.get("region", "eu-central-1"))

        table_name = os.environ["target_table"]

        _LOG.info(f"Table: {table_name}")
        table = dynamodb.Table(table_name)

        table.put_item(Item=obj)


HANDLER = Processor()

@xray_recorder.capture("lambda_handler")
def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
