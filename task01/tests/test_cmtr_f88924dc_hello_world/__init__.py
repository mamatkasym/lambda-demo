import unittest
import importlib
from tests import ImportFromSourceContext

with ImportFromSourceContext():
    LAMBDA_HANDLER = importlib.import_module('lambdas.cmtr-f88924dc-hello-world.handler')


class CmtrF88924dcHelloWorldLambdaTestCase(unittest.TestCase):
    """Common setups for this lambda"""

    def setUp(self) -> None:
        self.HANDLER = LAMBDA_HANDLER.CmtrF88924dcHelloWorld()

