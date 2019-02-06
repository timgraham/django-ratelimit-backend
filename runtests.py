#!/usr/bin/env python
import os
import sys

from django.conf import settings
from django.test.runner import DiscoverRunner
from django.utils.functional import empty


def setup_test_environment():
    # reset settings
    settings._wrapped = empty

    apps = [
        'django.contrib.sessions',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sites',
        'django.contrib.admin',
        'django.contrib.messages',
        'ratelimitbackend',
        'tests',
    ]
    settings_dict = {
        "DATABASES": {
            'default': {
                'ENGINE': "django.db.backends.sqlite3",
                'NAME': 'ratelimitbackend.sqlite',
            },
        },
        "CACHES": {
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            },
        },
        "ROOT_URLCONF": "tests.urls",
        "MIDDLEWARE": [
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'ratelimitbackend.middleware.RateLimitMiddleware',
        ],
        "INSTALLED_APPS": apps,
        "SITE_ID": 1,
        "AUTHENTICATION_BACKENDS": (
            'ratelimitbackend.backends.RateLimitModelBackend',
        ),
        "LOGGING": {
            'version': 1,
            'handlers': {
                'null': {
                    'class': 'logging.NullHandler',
                }
            },
            'loggers': {
                'ratelimitbackend': {
                    'handlers': ['null'],
                },
            },
        },
        "TEMPLATES": [{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'OPTIONS': {
                'loaders': (
                    'django.template.loaders.app_directories.Loader',
                ),
                'context_processors': (
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ),
            },
        }],
    }
    # set up settings for running tests for all apps
    settings.configure(**settings_dict)
    from django import setup
    setup()


def runtests():
    setup_test_environment()

    parent = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, parent)

    runner = DiscoverRunner(verbosity=1, interactive=True, failfast=False)
    failures = runner.run_tests(())
    sys.exit(failures)


if __name__ == '__main__':
    runtests()
