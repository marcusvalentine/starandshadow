# Django settings for starshadow project.

from settings_local import *

import os

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

TEMPLATE_DEBUG = DEBUG
SOUTH_TESTS_MIGRATE = False

ADMINS = (
    ('Simon Key', 'sjk@psimonkey.org.uk'),
)
MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
USE_TZ = True
TIME_ZONE = 'Europe/London'

import warnings

warnings.filterwarnings(
    'error', r"DateTimeField received a naive datetime",
    RuntimeWarning, r'django\.db\.models\.fields')

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-gb'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = False

DATE_FORMAT = 'l j F Y'
TIME_FORMAT = 'g:i a'
DATETIME_FORMAT = 'g:i a l j F Y'
SHORT_DATE_FORMAT = 'Y-m-d'
SHORT_TIME_FORMAT = 'H:i'
SHORT_DATETIME_FORMAT = 'Y-m-d H:i'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'static')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
#ADMIN_MEDIA_PREFIX = '/admin/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'o3!=64qxq(8v%e9n62zu8zj#d0xdyajpic^-gopwhwu46t8$4h'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'reversion.middleware.RevisionMiddleware',
    'ss.lib.middleware.SSMiddleware',
)

CACHE_MIDDLEWARE_SECONDS = 3600
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    "content.context_processors.menus",
    "content.context_processors.authenticated",
)

ROOT_URLCONF = 'ss.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/org/on/'

#TASTYPIE_ALLOW_MISSING_SLASH = True

ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_OPEN = True
AUTH_PROFILE_MODULE = 'programming.Programmer'

FIXTURE_DIRS = [
    os.path.join(PROJECT_ROOT, 'fixtures'),
]

STATIC_URL = '/static/'

COMPRESS_ENABLED = not DEBUG

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'south',
    'reversion',
    'compressor',
    'menus',
    'programming',
    'tastypie',
    'content',
    'fileupload',
    'organisation',
    'registration',
    'sorl.thumbnail',
)
