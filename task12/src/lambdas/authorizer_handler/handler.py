import re

import jwt
from commons.log_helper import get_logger

_LOG = get_logger(__name__, level="INFO")

SECRET = "tutorial_secret"
TOKEN = "Bearer "


#################################
#### This code is for later  ####
# def encode():
#     """
#     encode user payload as a jwt
#     :param user:
#     :return:
#     """
#     encoded_data = jwt.encode(
#         payload={"name": "some name"}, key=SECRET, algorithm="HS256"
#     )

#     return encoded_data

# encoding = encode()
# TOKEN = TOKEN + encoding
# _LOG.info(TOKEN)
##################################

def decode_auth_token(auth_token: str):
    """Decodes the auth token"""
    try:
        # remove "Bearer " from the token string.
        auth_token = auth_token.replace("Bearer ", "")
        # decode using secret key, will crash if not set.
        _LOG.info(auth_token)
        return "Fake success"
        # return jwt.decode(jwt=auth_token, key=SECRET, algorithms=["HS256"])

    except Exception:
        _LOG.info("Invalid token. Please log in again.")
        return


# encoding = encode()
# TOKEN = TOKEN + encoding


def lambda_handler(event, context):
    _LOG.info("Client token: " + event["authorizationToken"])
    _LOG.info("Method ARN: " + event["methodArn"])

    """
    Validate the incoming token and produce the principal user identifier
    associated with the token. This can be accomplished in a number of ways:

    1. Call out to the OAuth provider
    2. Decode a JWT token inline
    3. Lookup in a self-managed DB
    """

    user_details = decode_auth_token(event["authorizationToken"])
    _LOG.info(user_details)
    if user_details:
        principalId = "user|a1b2c3d4"
        tmp = event["methodArn"].split(":")
        apiGatewayArnTmp = tmp[5].split("/")
        awsAccountId = tmp[4]

        policy = AuthPolicy(principalId, awsAccountId)
        policy.restApiId = apiGatewayArnTmp[0]
        policy.region = tmp[3]
        policy.stage = apiGatewayArnTmp[1]
        # policy.denyAllMethods()
        policy.allowMethod(HttpVerb.GET, "/testing-autherizer")
        # policy.allowAllMethods()
        # Finally, build the policy
        authResponse = policy.build()

        return authResponse


class HttpVerb:
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    HEAD = "HEAD"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"
    ALL = "*"


class AuthPolicy(object):
    # The AWS account id the policy will be generated for. This is used to create the method ARNs.
    awsAccountId = ""
    # The principal used for the policy, this should be a unique identifier for the end user.
    principalId = ""
    # The policy version used for the evaluation. This should always be '2012-10-17'
    version = "2012-10-17"
    # The regular expression used to validate resource paths for the policy
    pathRegex = "^[/.a-zA-Z0-9-\*]+$"

    """Internal lists of allowed and denied methods.

    These are lists of objects and each object has 2 properties: A resource
    ARN and a nullable conditions statement. The build method processes these
    lists and generates the approriate statements for the final policy.
    """
    allowMethods = []
    denyMethods = []

    """Replace the placeholder value with a default API Gateway API id to be used in the policy.
    Beware of using '*' since it will not simply mean any API Gateway API id, because stars will greedily expand over '/' or other separators.
    See https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_resource.html for more details."""
    restApiId = "<<restApiId>>"

    """Replace the placeholder value with a default region to be used in the policy.
    Beware of using '*' since it will not simply mean any region, because stars will greedily expand over '/' or other separators.
    See https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_resource.html for more details."""
    region = "<<region>>"

    """Replace the placeholder value with a default stage to be used in the policy.
    Beware of using '*' since it will not simply mean any stage, because stars will greedily expand over '/' or other separators.
    See https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_resource.html for more details."""
    stage = "<<stage>>"

    def __init__(self, principal, awsAccountId):
        self.awsAccountId = awsAccountId
        self.principalId = principal
        self.allowMethods = []
        self.denyMethods = []

    def _addMethod(self, effect, verb, resource, conditions):
        """Adds a method to the internal lists of allowed or denied methods. Each object in
        the internal list contains a resource ARN and a condition statement. The condition
        statement can be null."""
        if verb != "*" and not hasattr(HttpVerb, verb):
            raise NameError(
                "Invalid HTTP verb " + verb + ". Allowed verbs in HttpVerb class"
            )
        resourcePattern = re.compile(self.pathRegex)
        if not resourcePattern.match(resource):
            raise NameError(
                "Invalid resource path: "
                + resource
                + ". Path should match "
                + self.pathRegex
            )

        if resource[:1] == "/":
            resource = resource[1:]

        resourceArn = "arn:aws:execute-api:{}:{}:{}/{}/{}/{}".format(
            self.region, self.awsAccountId, self.restApiId, self.stage, verb, resource
        )

        if effect.lower() == "allow":
            self.allowMethods.append(
                {"resourceArn": resourceArn, "conditions": conditions}
            )
        elif effect.lower() == "deny":
            self.denyMethods.append(
                {"resourceArn": resourceArn, "conditions": conditions}
            )

    def _getEmptyStatement(self, effect):
        """Returns an empty statement object prepopulated with the correct action and the
        desired effect."""
        statement = {
            "Action": "execute-api:Invoke",
            "Effect": effect[:1].upper() + effect[1:].lower(),
            "Resource": [],
        }

        return statement

    def _getStatementForEffect(self, effect, methods):
        """This function loops over an array of objects containing a resourceArn and
        conditions statement and generates the array of statements for the policy."""
        statements = []

        if len(methods) > 0:
            statement = self._getEmptyStatement(effect)

            for curMethod in methods:
                if curMethod["conditions"] is None or len(curMethod["conditions"]) == 0:
                    statement["Resource"].append(curMethod["resourceArn"])
                else:
                    conditionalStatement = self._getEmptyStatement(effect)
                    conditionalStatement["Resource"].append(curMethod["resourceArn"])
                    conditionalStatement["Condition"] = curMethod["conditions"]
                    statements.append(conditionalStatement)

            if statement["Resource"]:
                statements.append(statement)

        return statements

    def allowAllMethods(self):
        """Adds a '*' allow to the policy to authorize access to all methods of an API"""
        self._addMethod("Allow", HttpVerb.ALL, "*", [])

    def denyAllMethods(self):
        """Adds a '*' allow to the policy to deny access to all methods of an API"""
        self._addMethod("Deny", HttpVerb.ALL, "*", [])

    def allowMethod(self, verb, resource):
        """Adds an API Gateway method (Http verb + Resource path) to the list of allowed
        methods for the policy"""
        self._addMethod("Allow", verb, resource, [])

    def denyMethod(self, verb, resource):
        """Adds an API Gateway method (Http verb + Resource path) to the list of denied
        methods for the policy"""
        self._addMethod("Deny", verb, resource, [])

    def allowMethodWithConditions(self, verb, resource, conditions):
        """Adds an API Gateway method (Http verb + Resource path) to the list of allowed
        methods and includes a condition for the policy statement. More on AWS policy
        conditions here: http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html#Condition
        """
        self._addMethod("Allow", verb, resource, conditions)

    def denyMethodWithConditions(self, verb, resource, conditions):
        """Adds an API Gateway method (Http verb + Resource path) to the list of denied
        methods and includes a condition for the policy statement. More on AWS policy
        conditions here: http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html#Condition
        """
        self._addMethod("Deny", verb, resource, conditions)

    def build(self):
        """Generates the policy document based on the internal lists of allowed and denied
        conditions. This will generate a policy with two main statements for the effect:
        one statement for Allow and one statement for Deny.
        Methods that includes conditions will have their own statement in the policy."""
        if (self.allowMethods is None or len(self.allowMethods) == 0) and (
                self.denyMethods is None or len(self.denyMethods) == 0
        ):
            raise NameError("No statements defined for the policy")

        policy = {
            "principalId": self.principalId,
            "policyDocument": {"Version": self.version, "Statement": []},
        }

        policy["policyDocument"]["Statement"].extend(
            self._getStatementForEffect("Allow", self.allowMethods)
        )
        policy["policyDocument"]["Statement"].extend(
            self._getStatementForEffect("Deny", self.denyMethods)
        )

        return policy