import json

from tests.test_hello_world import HelloWorldLambdaTestCase


class TestSuccess(HelloWorldLambdaTestCase):

    def test_success(self):
        self.assertEqual(
            self.HANDLER.handle_request({"requestContext": {"http": {"method": "GET", "path": "/hello"}}}, dict()), {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({
                    "statusCode": 200,
                    "message": "Hello from Lambda"
                })
            })

    def test_fail_wrong_request_method(self):
        self.assertEqual(
            self.HANDLER.handle_request({"requestContext": {"http": {"method": "POST", "path": "/hello"}}}, dict()), {

                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({
                    "statusCode": 400,
                    "message": "Bad request syntax or unsupported method. Request path: /hello. HTTP method: POST"
                })
            })

    def test_fail_wrong_path(self):
        self.assertEqual(
            self.HANDLER.handle_request({"requestContext": {"http": {"method": "GET", "path": "/goodbye"}}}, dict()), {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({
                    "statusCode": 400,
                    "message": "Bad request syntax or unsupported method. Request path: /goodbye. HTTP method: GET"
                })
            })

    def test_fail_empty_path(self):
        self.assertEqual(self.HANDLER.handle_request(dict(), dict()), {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "statusCode": 400,
                "message": "Bad request syntax or unsupported method. Request path: None. HTTP method: None"
            })
        })
