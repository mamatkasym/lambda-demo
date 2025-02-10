import datetime
import json
import os
import uuid

import boto3
from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger(__name__)


class UuidGenerator(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass

    def handle_request(self, event, context):
        """
        Explain incoming event here
        """
        # todo implement business logic
        if "time" in event:
            _LOG.info("Event accepted.")
            file_name = datetime.datetime.now().isoformat()
            s3_client = boto3.client('s3')
            data = {"ids": [uuid.uuid4().hex for _ in range(10)]}
            bucket = os.environ["target_bucket"]
            _LOG.info(f"BUCKET: {bucket}")
            s3_client.put_object(Body=json.dumps(data), Bucket=bucket,
                                 Key=file_name)


HANDLER = UuidGenerator()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
