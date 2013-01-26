from cStringIO import StringIO
from django.test import TestCase
from django.conf import settings
from django_upyun import UpYunStorage
import requests


class ApiTest(TestCase):
    def setUp(self):
        self.storage = UpYunStorage()

    def _craete_file(self, content):
        return StringIO(content)

    def test_create(self):
        name = 'hello.html'
        content = '<h1>Hello World</h1>'

        file = self._craete_file(content)

        self.storage.save(name, file)
        self.assertEqual(self.storage.url(name), name)

        self.assertTrue(self.storage.exists(name))

        self.assertEqual(self.storage.open(name).read(), content)
        public_url = settings.MEDIA_URL + self.storage.url(name)
        self.assertEqual(requests.get(public_url).content, content)

        # self.storage.delete(name)
        # self.assertFalse(self.storage.exists(name))

    def test_404(self):
        name = "__404__"
        file = self.storage.open(name)
        self.assertRaises(IOError, lambda: file.read())
