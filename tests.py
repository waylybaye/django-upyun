import os
import sys
from django.conf import settings

BASE_PATH = os.path.dirname(__file__)


def main():
    """
    Standalone django model test with a 'memory-only-django-installation'.
    You can play with a django model without a complete django app installation.
    http://www.djangosnippets.org/snippets/1044/
    """
    settings.configure(
        INSTALLED_APPS = (
            'django.contrib.auth',
            'django.contrib.sessions',
            'django.contrib.contenttypes',
            'django_upyun',
        ),
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        ROOT_URLCONF='beproud.django.authutils.tests.test_urls',
        DEFAULT_FILE_STORAGE = 'django_upyun.UpYunStorage'
    )

    from django.test.utils import get_runner
    test_runner = get_runner(settings)(verbosity=2, interactive=True)
    failures = test_runner.run_tests(['django_upyun'])
    sys.exit(failures)

if __name__ == '__main__':
    main()
