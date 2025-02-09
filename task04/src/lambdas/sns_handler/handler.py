from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger(__name__)


class SnsHandler(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass

    # Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
    # SPDX-License-Identifier: Apache-2.0
    def lambda_handler(self, event, context):
        for record in event['Records']:
            self.process_message(record)

    def process_message(self, record):
        try:
            message = record['Sns']['Message']
            _LOG.info(f"{message}")

        except Exception as e:
            _LOG.info("An error occurred")


HANDLER = SnsHandler()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
