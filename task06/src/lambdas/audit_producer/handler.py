import datetime
import os
import uuid

import boto3
from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger(__name__)


class AuditProducer(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass

    def handle_record(self, record):
        method = record["eventName"]
        dynamodb = boto3.resource('dynamodb', region_name=os.environ.get("region", "eu-central-1"))
        table_names = sorted([table.name for table in list(dynamodb.tables.all()) if "cmtr-f88924dc-Audit" in table.name], key=lambda z: len(z))
        table_name = table_names[-1].replace("Table", "")

        _LOG.info(f"Table: {table_name}")
        table = dynamodb.Table(table_name)
        new_image = record["dynamodb"]["NewImage"]
        obj = {"id": uuid.uuid4().hex}

        if method == "INSERT":
            obj = {
                       "id": uuid.uuid4().hex,
                       "itemKey": new_image["key"],
                       "modificationTime": datetime.datetime.now().isoformat(),
                       "newValue": {
                           "key": new_image["key"],
                           "value": new_image["value"],
                       },
                    }
        elif method == "MODIFY":
            old_image = record["dynamodb"]["OldImage"]
            obj = {
                       "id": uuid.uuid4().hex,
                       "itemKey": new_image["key"],
                       "modificationTime": datetime.datetime.now().isoformat(),
                       "updatedAttribute": "value",
                       "oldValue": old_image["value"],
                       "newValue": new_image["value"]
                    }

        table.put_item(Item=obj)

    def handle_request(self, event, context):
        """
        Explain incoming event here
        """
        # todo implement business logic
        _LOG.info(f"EVENT: {event}")

        for record in event["Records"]:
            _LOG.info(record)
            self.handle_record(record)
    

HANDLER = AuditProducer()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
