django-upyun
=============

django storage for [又拍云存储](http://upyun.com)

## INSTALL

```sh
$ pip install django-upyun-storage
```

## USAGE

修改 `settings.py`

```python
UPYUN_BUCKET = "空间名称"
UPYUN_ACCOUNT = "操作员用户名"
UPYUN_PASSWORD = "操作员密码"
STATICFILES_STORAGE = 'django_upyun.storage.UpYunStorage'
```

### 将静态文件上传到又拍云CDN

```sh
$ python manage.py collectstatic
```
