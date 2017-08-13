"""
Django settings for zabbix_rules project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import djcelery
djcelery.setup_loader()
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ROOT_DIR = os.getcwd()
LOG_DIR = ROOT_DIR + "/log"

BROKER_URL = "amqp://zabbix_rules:zabbix_rules@localhost:5672/zabbix_rules"
CELERYD_MAX_TASKS_PER_CHILD = 20000
CELERYD_PREFETCH_MULTIPLIER = 30
CELERY_ACKS_LATE = True
CELERY_ANNOTATIONS = {"*": {"rate_limit": "10/s"}}
CELERY_IGNORE_RESULT = False
CELERY_IMPORTS = ("rules_celery.tasks", )
CELERY_RESULT_BACKEND = "amqp"
CELERY_TASK_RESULT_EXPIRES = 3600
CELERY_AMQP_TASK_RESULT_EXPIRES = 1000

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '686_-56t4^nxv8yl&367ik80=7vtzotd*4u0c1f@nkoa1idg5-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djcelery',
    'rules_celery',
    'zabbix_rules'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'zabbix_rules.urls'

WSGI_APPLICATION = 'zabbix_rules.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'zabbix_rules',                # Or path to database file if using sqlite3.
        'USER': 'zabbix',                      # Not used with sqlite3.
        'PASSWORD': 'zabbix',                  # Not used with sqlite3.
        'HOST': 'localhost',                   # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3808',                      # Set to empty string for default. Not used with sqlite3.    }
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

ZABBIX_URL = [
    'http://zabbix-server.example.com/',
]

ZABBIX_DB = {
    'db': 'zabbix',
    'user': 'zabbix',
    'pass': 'zabbix',
    'server': 'localhost',
    'port': 3808
}

ZABBIX_API = {
    'url': 'http://zabbix-server.example.com/',
    'user': 'user',
    'pass': 'password'
}
