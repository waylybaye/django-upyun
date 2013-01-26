try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = __import__('django_upyun').__version__

setup(
    name="django-upyun",
    packages=['django_upyun'],
    version=version,
    author="Baye Wayly",
    author_email="havelove@gmail.com",
    url="https://github.com/waylybaye/django-upyun",
    tests_require=['Django', 'python-dateutil', 'requests'],
    test_suite='tests.main',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],
)
