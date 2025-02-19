import unittest


class TestSuccess(unittest.TestCase):

    def test_success(self):
        self.assertEqual(200, 200)

