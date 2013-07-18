try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = __import__('django_upyun').__version__

setup(
    name="django-upyun-storage",
    description="django storage for upyun.com",
    packages=['django_upyun'],
    version=version,
    author="Baye Wayly",
    author_email="baye@wayly.net",
    url="https://github.com/waylybaye/django-upyun",
    install_requires=["requests", "python-dateutil"],
    license="MIT",
    tests_require=['Django', 'python-dateutil', 'requests'],
    test_suite='tests.main',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],
)
