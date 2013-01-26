import os
from django.conf import settings
from django.core.files.storage import Storage
from dateutil import parser, tz
import requests


VERSION = (0, 0, 1, 'alpha')

# Dynamically calculate the version based on VERSION tuple
if len(VERSION) > 2 and VERSION[2] is not None:
    if isinstance(VERSION[2], int):
        str_version = "%s.%s.%s" % VERSION[:3]
    else:
        str_version = "%s.%s_%s" % VERSION[:3]
else:
    str_version = "%s.%s" % VERSION[:2]

__version__ = str_version


class UpYunStorage(Storage):
    """
    UpYun Storage
    """
    def __init__(self, options=None):
        if not options:
            self.account = settings.UPYUN_ACCOUNT
            self.password = settings.UPYUN_PASSWORD
            self.bucket = settings.UPYUN_BUCKET
            self.api_url = "http://v2.api.upyun.com"
            self.cache = {}

    def _open(self, name, mode="rb"):
        path = os.path.join(settings.COMPRESS_ROOT, name)
        return file(path, mode)

    def _get_url(self, name):
        return "%s/%s/%s/%s" % (self.api_url, self.bucket, settings.STATIC_VERSION, name)

    def _save(self, name, content):
        file_data = content.read()
        headers = {
            'Mkdir': 'true',
        }
        url = self._get_url(name)
        requests.put(url, file_data, headers=headers, auth=(self.account, self.password))
        return name

    def delete(self, name):
        pass

    def save(self, name, content):
        return self._save(name, content)

    def modified_time(self, name):
        url = self._get_url(name)
        resp = self.cache[url]

        last_modified_date = parser.parse(resp.headers.get('date'))

        # if the date has no timzone, assume UTC
        if last_modified_date.tzinfo == None:
            last_modified_date = last_modified_date.replace(tzinfo=tz.tzutc())

        # convert date to local time w/o timezone
        return last_modified_date.astimezone(tz.tzlocal()).replace(tzinfo=None)

    def exists(self, name):
        url = self._get_url(name)
        resp = self.request('get', url)
        self.cache[url] = resp

        if resp.status_code == 200:
            return True

        elif resp.status_code == 404:
            return False

        raise Exception("Unknown status code")

    def listdir(self, path):
        pass

    def request(self, method, url):
        return requests.request(method, url, auth=(self.account, self.password))

    def size(self, name):
        pass

    def url(self, name):
        return self._get_url(name)

