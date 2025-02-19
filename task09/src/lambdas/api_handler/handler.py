from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

import requests

_LOG = get_logger(__name__)


class ApiHandler(AbstractLambda):

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

        request_context = event.get("requestContext", {})
        request = request_context.get("http", {})
        method = request.get("method")
        path = request.get("path")
        _LOG.info(f"{path} | {method}")
        if path == '/weather' and method == "GET":
            response = requests.get(
                "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m")

            return response.json()

        _LOG.info("Return 400 response")
        return {
            "statusCode": 400,
            "message": f"Bad request syntax or unsupported method. Request path: {path}. HTTP method: {method}"
        }


HANDLER = ApiHandler()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
