from django.conf import settings
from django.core.files import File
from django.core.files.storage import Storage
from dateutil import parser, tz
import requests

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


class UpYunStorage(Storage):
    """
    UpYun Storage
    """
    def __init__(self, account=None, password=None, bucket=None):
        self.account = account or settings.UPYUN_ACCOUNT
        self.password = password or settings.UPYUN_PASSWORD
        self.bucket = bucket or settings.UPYUN_BUCKET
        self.api_url = "http://v0.api.upyun.com"
        self.cache = {}

    def _endpoint(self, bucket_name):
        return "%s/%s/%s" % (self.api_url, self.bucket, bucket_name)

    def _request(self, method, url, data=None, **kwargs):
        return requests.request(method, url, data=data, auth=(self.account, self.password), **kwargs)

    def _open(self, name, mode="rb"):
        file = UpYunFile(name, self, mode)
        self.cache[name] = file
        return file

    def _save(self, name, content):
        file_data = content.read()
        headers = {
            'Mkdir': 'true',
        }
        url = self._endpoint(name)
        # requests.put(url, file_data, headers=headers, auth=(self.account, self.password))
        resp = self._request('PUT', url, file_data, headers=headers)
        if not resp.status_code == 200:
            raise IOError("UpYunStorageError: %s" % resp.content)
        return name

    def delete(self, name):
        url = self._endpoint(name)
        resp = self._request("DELETE", url)
        if not resp.content == 'true':
            raise IOError("UpYunStorageError: failed to delete file")

    def save(self, name, content):
        return self._save(name, content)

    def modified_time(self, file_name):
        url = self._endpoint(file_name)
        resp = self.cache.get(url) or self._request('HEAD', url)

        last_modified_date = parser.parse(resp.headers.get('date'))

        # if the date has no timzone, assume UTC
        if last_modified_date.tzinfo is None:
            last_modified_date = last_modified_date.replace(tzinfo=tz.tzutc())

        # convert date to local time w/o timezone
        return last_modified_date.astimezone(tz.tzlocal()).replace(tzinfo=None)

    def exists(self, name):
        url = self._endpoint(name)
        resp = self._request('HEAD', url)
        return resp.status_code == 200

    def size(self, name):
        if name in self.cache:
            return self.cache[name].size
        url = self._endpoint(name)
        return self._request('HEAD', url).headers.get('Content-Length')

    def _read(self, name):
        url = self._endpoint(name)
        resp = self._request('GET', url)
        if resp.status_code == 200:
            return resp.content
        elif resp.status_code == 404:
            raise IOError("File not found")
        else:
            raise IOError("UpYunStorageError: Unknown Error when read file, code %s" % resp.status_code)

    def url(self, name):
        return name


class UpYunFile(File):
    def __init__(self, name, storage, mode):
        self._name = name
        self._storage = storage
        self._mode = mode
        self.file = StringIO()
        self._is_dirty = False

    @property
    def size(self):
        if not hasattr(self, '_size'):
            self._size = self._storage.size(self._name)
        return self._size

    def read(self):
        data = self._storage._read(self._name)
        self.file = StringIO(data)
        return self.file.getvalue()

    def write(self, content):
        if 'w' not in self._mode:
            raise AttributeError("File was opened for read-only access.")
        self.file = StringIO(content)
        self._is_dirty = True

    def close(self):
        if self._is_dirty:
            self._storage._put_file(self._name, self.file.getvalue())
        self.file.close()
