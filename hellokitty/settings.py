"""
Django settings for hellokitty project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from local_settings import *
from hellokitty.common.appconfig import *
from datetime import timedelta
import sys
import djcelery


PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))

CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
reload(sys)
sys.setdefaultencoding('utf-8')
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DEFAULT_CHARSET = 'utf-8'

djcelery.setup_loader()
BASE_DIR = BASE_DIR + '/hellokitty'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$)5+@9ou+z$k51+m$e@c+x^@0g89o!a4j0-76d+er4j8wq)!1d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'hellokitty.apps.torrentkitty',
    'djcelery',
    'djsupervisor',
    'south'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'hellokitty.urls'

WSGI_APPLICATION = 'hellokitty.wsgi.application'


MEDIA_ROOT = os.path.join(BASE_DIR, 'static/').replace('\\', '/')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static').replace('\\', '/')

STATIC_URL = '/static/'
# Additional locations of static files
base_locale_path = os.path.dirname(os.path.dirname(__file__))
LOCALE_PATHS = (
    os.path.join(base_locale_path, 'locale').replace('\\', '/'),
)

STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    ("css", os.path.join(STATIC_ROOT, 'css')),
    ("js", os.path.join(STATIC_ROOT, 'js')),
    ("images", os.path.join(STATIC_ROOT, 'images')),
    ("upload", os.path.join(STATIC_ROOT, 'upload')),
    ("fonts", os.path.join(STATIC_ROOT, 'fonts')),
    ("webuploader", os.path.join(STATIC_ROOT, 'webuploader')),
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or
    # "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # '/home/looen/workspace/coin2b/templates/',
    os.path.join(BASE_DIR, 'templates/').replace('\\', '/'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
)

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

BROKER_URL = 'redis://localhost:6379/0'

CELERYBEAT_SCHEDULE = {
    "robot": {
        "task": "hellokitty.apps.torrentkitty.tasks.get_root_port",
        "schedule": timedelta(hours=4),
    },
    "resources": {
        "task": "hellokitty.apps.torrentkitty.tasks.get_resources_and_page",
        "schedule": timedelta(hours=4),
    }
}
