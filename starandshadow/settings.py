# Django settings for starshadow project.

from settings_local import *

import os

PROJECT_ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')

TEMPLATE_DEBUG = DEBUG
SOUTH_TESTS_MIGRATE = False

ADMINS = (
    ('Simon Key', 'sjk@psimonkey.org.uk'),
)
MANAGERS = ADMINS

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-gb'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

import warnings

warnings.filterwarnings(
    'error', r"DateTimeField received a naive datetime",
    RuntimeWarning, r'django\.db\.models\.fields')

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
MEDIA_URL = '/media/'

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
    'lib.middleware.SSMiddleware',
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

ROOT_URLCONF = 'starandshadow.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'starandshadow.wsgi.application'

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
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)
STATICFILES_ROOT = os.path.join(PROJECT_ROOT, 'static')
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)
STATIC_URL = '/static/'

#COMPRESS_ENABLED = not DEBUG
COMPRESS_ENABLED = True
COMPRESS_PRECOMPILERS = (
    ('text/coffeescript', 'coffee --compile --stdio'),
    ('text/less', 'lessc {infile} {outfile}'),
    ('text/x-sass', 'sass {infile} {outfile}'),
    ('text/x-scss', 'sass --scss {infile} {outfile}'),
    ('text/stylus', 'stylus < {infile} > {outfile}'),
    ('text/foobar', 'path.to.MyPrecompilerFilter'),
)
COMPRESS_ROOT = os.path.join(PROJECT_ROOT, 'static')
COMPRESS_OUTPUT_DIR = 'cache'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
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

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
