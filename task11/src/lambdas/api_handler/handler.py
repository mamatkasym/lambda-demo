import json
import os
import uuid
from decimal import Decimal

import boto3
from botocore.exceptions import ClientError
from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger(__name__, level="INFO")


class ApiHandler(AbstractLambda):
    user_pool = os.environ.get("booking-userpool")

    def __init__(self):
        _LOG.info(f"ENV VARIABLES: {os.environ.items()}")
        self.cognito_idp_client = boto3.client("cognito-idp", region_name=os.environ.get("region", "eu-central-1"))
        self.cognito_userpool_id = os.environ.get("cognito_userpool_id")
        self.cognito_client_id = os.environ.get("cognito_client_id")
        dynamodb = boto3.resource('dynamodb', region_name=os.environ.get("region", "eu-central-1"))
        tables_table_name = os.environ.get("tables_table")

        _LOG.info(f"Tables table: {tables_table_name}")
        self.tables_table = dynamodb.Table(tables_table_name)

        reservations_table_name = os.environ.get("reservations_table")

        _LOG.info(f"Reservations table: {reservations_table_name}")
        self.reservations_table = dynamodb.Table(reservations_table_name)
    def validate_request(self, event) -> dict:
        pass

    def signin(self, event):
        body = json.loads(event["body"])

        username = body.get("email")
        password = body.get("password")
        try:
            kwargs = {
                "UserPoolId": self.cognito_userpool_id,
                "ClientId": self.cognito_client_id,
                "AuthFlow": "ADMIN_USER_PASSWORD_AUTH",
                "AuthParameters": {"USERNAME": username, "PASSWORD": password},
            }

            response = self.cognito_idp_client.admin_initiate_auth(**kwargs)
            _LOG.info(f"Admin initiate auth response: {response}")
            challenge_name = response.get("ChallengeName", None)
            if challenge_name == "MFA_SETUP":
                if (
                    "SOFTWARE_TOKEN_MFA"
                    in response["ChallengeParameters"]["MFAS_CAN_SETUP"]
                ):
                    response.update(self.get_mfa_secret(response["Session"]))
                else:
                    raise RuntimeError(
                        "The user pool requires MFA setup, but the user pool is not "
                        "configured for TOTP MFA. This example requires TOTP MFA."
                    )
        except ClientError as err:
            _LOG.info(
                f"[ERROR] Couldn't start sign in for {username}. Here's why: {err.response['Error']['Code']}: {err.response['Error']['Message']}"
            )
            return {"statusCode": 400}
        except Exception as e:
            _LOG.info("[EXCEPTION] {e}")
            return {"statusCode": 400}
        else:

            access_token = response["AuthenticationResult"]["IdToken"]
            _LOG.info(f"Access Token: {access_token}")

            return {"statusCode": 200, "body": json.dumps({"accessToken": access_token})}

    def signup(self, event):
        # Access user attributes from the event payload

        # username = event['request']['userAttributes']['username']
        body: dict = json.loads(event.get("body"))
        _LOG.info(f"BODY: {body}")
        username = body.get("email")
        password = body.pop("password")

        attributes = []
        for k, v in body.items():
            attributes.append({"Name": k, "Value": v})
        _LOG.info(f"ATTRIBUTES: {attributes}")

        try:
            kwargs = {
                "ClientId": self.cognito_client_id,
                'Username': username,
                "Password": password,
                "UserAttributes": [{"Name": "email", "Value": username}]
            }
            response = self.cognito_idp_client.sign_up(**kwargs)
            _LOG.info(f"Signup response: {response}")
            response = self.cognito_idp_client.admin_confirm_sign_up(
                UserPoolId=self.cognito_userpool_id, Username=username)
            _LOG.info(f"Confirm Signup response: {response}")
            confirmed = True
        except ClientError as err:
            if err.response["Error"]["Code"] == "UsernameExistsException":
                response = self.cognito_idp_client.admin_get_user(
                    UserPoolId=self.cognito_userpool_id, Username=username
                )
                _LOG.info(
                    f"[WARN] User {username} exists and is {response['UserStatus']}."
                )
                _LOG.info(f"Get user response: {response}")
                confirmed = response["UserStatus"] == "CONFIRMED"
            else:
                _LOG.info(
                    f"[ERROR] Couldn't sign up {username}. Here's why: {err.response['Error']['Code']}: {err.response['Error']['Message']}",

                )
                return {"statusCode": 400}

        return {"statusCode": 200} if confirmed else {"statusCode": 400}

    def create_table(self, event: dict):

        body = json.loads(event.get("body"))

        try:
            self.tables_table.put_item(Item=body)

            return {
                "statusCode": 200,
                "body": json.dumps({"id": body["id"]}, default=float)
            }
        except Exception as e:
            _LOG.error(e)
            return {
                "statusCode": 400
            }

    def list_tables(self):
        _LOG.info("List Tables...")
        _LOG.error("TEST ERROR LOG...")

        tables = []
        scan_kwargs = {}
        try:
            done = False
            start_key = None
            while not done:
                if start_key:
                    scan_kwargs["ExclusiveStartKey"] = start_key
                response = self.tables_table.scan(**scan_kwargs)
                tables.extend(response.get("Items", []))
                start_key = response.get("LastEvaluatedKey", None)
                done = start_key is None
            _LOG.info(f"Done scanning table Tables. Number of records: {len(tables)}")
        except ClientError as err:
            _LOG.error(f"{err}")
            _LOG.info(
                f"[ERROR] Couldn't scan for movies. Here's why: {err.response['Error']['Code']}: {err.response['Error']['Message']}",
            )
            return {
                "statusCode": 400
            }
        except Exception as e:
            _LOG.info(f"[EXCEPTION] {e}")

            return {
                "statusCode": 400
            }
        else:
            return {
                "statusCode": 200,
                "body": json.dumps({"tables": tables}, default=float)
            }

    def list_reservations(self):
        _LOG.info("List reservations...")
        reservations = []
        scan_kwargs = {}
        try:
            done = False
            start_key = None
            while not done:
                if start_key:
                    scan_kwargs["ExclusiveStartKey"] = start_key
                response = self.reservations_table.scan(**scan_kwargs)
                reservations.extend(response.get("Items", []))
                start_key = response.get("LastEvaluatedKey", None)
                done = start_key is None
            _LOG.info(f"Done scanning table Reservations. Number of records: {len(reservations)}")
        except ClientError as err:
            _LOG.info(
                f'[ERROR] Could not scan. Here is why: {err.response["Error"]["Code"]}: {err.response["Error"]["Message"]}',
            )
            return {
                "statusCode": 400
            }
        except Exception as e:
            _LOG.info(f"[EXCEPTION] {e}")
            return {
                "statusCode": 400
            }
        else:
            return {
                "statusCode": 200,
                "body": json.dumps({"reservations": reservations}, default=float)
            }

    def create_reservation(self, event: dict):
        body: dict = json.loads(event.get("body"))
        body.update({"id": uuid.uuid4().hex})
        reservation_id = body["id"]
        tableId = body.get("tableNumber")

        try:
            response = self.tables_table.get_item(Key={"id": tableId})
            if "Item" not in response:
                return {
                    "statusCode": 400
                }

            response = self.reservations_table.get_item(Key={"id": reservation_id})
            if "Item" in response:
                return {
                    "statusCode": 400
                }

            self.reservations_table.put_item(Item=body)
            _LOG.info("Reservation is created successfully...")

            return {
                "statusCode": 200,
                "body": json.dumps({"reservationId": reservation_id})
            }

        except ClientError as e:
            _LOG.error(e)
            return {
                "statusCode": 400
            }

    def get_table(self, event):
        path_params = event.get("pathParameters")
        table_id = int(path_params.get("tableId"))

        try:
            response = self.tables_table.get_item(Key={"id": table_id})
        except ClientError as err:
            _LOG.error(
                "Couldn't get table from table Tables. Here's why: %s: %s",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            return {
                "statusCode": 400
            }
        else:
            return {
                "statusCode": 200,
                "body": json.dumps(response["Item"], default=float)
            }
    def handle_request(self, event, context):
        """
        Explain incoming event here
        """
        _LOG.info(f"EVENT: {event}")

        method = event.get("httpMethod")
        path = event.get("path")
        resource = event.get("resource")
        _LOG.info(f"PATH: {path}")
        _LOG.info(f"METHOD: {method}")
        _LOG.info(f"RESOURCE: {resource}")

        if path == "/signup" and method == "POST":
            return self.signup(event)

        elif path == "/signin" and method == "POST":
            return self.signin(event)

        elif path == "/tables":
            if method == "POST":
                return self.create_table(event)
            elif method == "GET":
                return self.list_tables()

        elif path == "/reservations":
            if method == "POST":
                return self.create_reservation(event)
            elif method == "GET":
                return self.list_reservations()
        elif resource == "/tables/{tableId}":
            return self.get_table(event)

HANDLER = ApiHandler()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
