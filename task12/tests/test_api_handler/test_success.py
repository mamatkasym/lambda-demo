from unittest import TestCase


class TestSuccess(TestCase):

    def test_success(self):
        self.assertEqual(200, 200)

