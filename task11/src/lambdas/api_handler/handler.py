import os

import boto3
from botocore.exceptions import ClientError
from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger(__name__)


class ApiHandler(AbstractLambda):
    user_pool = os.environ.get("booking-userpool")

    def validate_request(self, event) -> dict:
        pass

    def signup(self, event):
        # Access user attributes from the event payload

        # username = event['request']['userAttributes']['username']

        email = event['request']['userAttributes']['email']
        username = email
        password = event['request']['userAttributes']['password']
        first_name = event['request']['userAttributes']['firstName']
        last_name = event['request']['userAttributes']['lastName']
        # Perform custom validation logic (e.g., check if email is already in use)


        try:
            kwargs = {
                "ClientId": self.user_pool,
                'Username': email,
                "Password": password,
                "UserAttributes": {
                    "email": email,
                    "firstName": first_name,
                    "lastName": last_name
                }
            }
            if self.client_secret is not None:
                kwargs["SecretHash"] = self._secret_hash(username)
            response = self.cognito_idp_client.sign_up(**kwargs)
            confirmed = response["UserConfirmed"]
        except ClientError as err:
            if err.response["Error"]["Code"] == "UsernameExistsException":
                response = self.cognito_idp_client.admin_get_user(
                    UserPoolId=self.user_pool, Username=username
                )
                _LOG.warning(
                    "User %s exists and is %s.", username, response["UserStatus"]
                )
                confirmed = response["UserStatus"] == "CONFIRMED"
            else:
                _LOG.error(
                    "Couldn't sign up %s. Here's why: %s: %s",
                    username,
                    err.response["Error"]["Code"],
                    err.response["Error"]["Message"],
                )
                raise
        return 200 if confirmed else 400

    def handle_request(self, event, context):
        """
        Explain incoming event here
        """
        _LOG.info(f"EVENT: {event}")
        _LOG.info(f"CONTEXT: {context}")
        request_context = event.get("requestContext", {})
        request = request_context.get("http", {})
        method = request.get("method")
        path = request.get("path")
        _LOG.info(f"PATH: {path}")

        if path == "/signup":
            return self.signup(event)
    

HANDLER = ApiHandler()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
