from tests.test_cmtr_f88924dc_hello_world import CmtrF88924dcHelloWorldLambdaTestCase


class TestSuccess(CmtrF88924dcHelloWorldLambdaTestCase):

    def test_success(self):
        self.assertEqual(self.HANDLER.handle_request(dict(), dict()), 200)

