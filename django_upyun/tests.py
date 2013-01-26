from django.test import TestCase
from django_upyun import UpYunStorage


class ApiTest(TestCase):
    def setUp(self):
        self.storage = UpYunStorage()

    def _create_random_file(self):
        pass

    def test_put(self):
        pass
