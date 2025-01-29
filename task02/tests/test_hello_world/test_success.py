import json

from tests.test_hello_world import HelloWorldLambdaTestCase


class TestSuccess(HelloWorldLambdaTestCase):

    def test_success(self):
        self.assertEqual(self.HANDLER.handle_request({"rawPath": "/hello"}, dict()), {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "statusCode": 200,
                "message": "Hello from Lambda"
            })
        })

    def test_fail(self):
        self.assertEqual(self.HANDLER.handle_request({"rawPath": "/goodbye"}, dict()), {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({
                    "statusCode": 400,
                    "message": "Bad request syntax or unsupported method. Request path: {path}. HTTP method: {method}"
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
                    "message": "Bad request syntax or unsupported method. Request path: {path}. HTTP method: {method}"
                })
            })

