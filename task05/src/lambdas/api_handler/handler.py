import datetime
import json
import os
import uuid

import boto3
from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger(__name__)


class ApiHandler(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass

    def handle_request(self, event, context):
        """
        Explain incoming event here
        """
        # todo implement business logic
        _LOG.info(f"EVENT: {event}")
        _LOG.info(f"ENVS: {os.environ.keys()}")
        for key in os.environ.keys():
            _LOG.info(f"{key}: {os.environ[key]}")

        principal_id = event.get("principalId")
        content = event.get("content")

        obj = {
            "id": str(uuid.uuid4()),
            "principalId": principal_id,
            "createdAt": str(datetime.datetime.now()),
            "body": content
        }

        dynamodb = boto3.resource('dynamodb', region_name=os.environ["region"])
        table_name = os.environ["table_name"]

        table = dynamodb.Table(table_name)

        table.put_item(Item=obj)

        return {
            "statusCode": 201,
            "event": json.dumps(obj, indent=4)
        }


HANDLER = ApiHandler()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
