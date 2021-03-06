# Django settings for mon project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

VERSION = "1.0.0"

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

import os, inspect
PROJECT_PATH = os.path.normpath(os.path.join(os.path.dirname(inspect.getfile(inspect.currentframe())), os.path.pardir))

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Moscow'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media/')

MEDIA_URL = '/media/'

STATIC_ROOT = ''

STATIC_URL = os.path.join(PROJECT_PATH, 'static/')

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ygke45m)avko^)jq_#x5j8xenl#$738fic#=p40vrqe=6y#6+)'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'mon.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'mon.wsgi.application'

TEMPLATE_DIRS = (os.path.join(PROJECT_PATH, 'mon/templates'),)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    # 'debug_toolbar',
    'fixture_magic',
    'apps.imgfile',
    'apps.core',
    'apps.mo',
    'apps.build',
    'apps.cmp',
    'apps.payment',
    'apps.user',
    'webodt',
    # 'debug_toolbar',
    'south',
    'autocomplete_light',
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

LOGIN_REDIRECT_URL = '/'

from mon.settings_local import DATABASES

if DEBUG:
    # MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    # INSTALLED_APPS += ('debug_toolbar',)
    INTERNAL_IPS = ('127.0.0.1',)
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
        'HIDE_DJANGO_SQL': False,
        'ENABLE_STACKTRACES' : True,
    }
#    MIDDLEWARE_CLASSES = list(MIDDLEWARE_CLASSES)
#    MIDDLEWARE_CLASSES.insert(0, 'mon.middleware.DisableCSRF')


WEBODT_CONVERTER = 'webodt.converters.abiword.AbiwordODFConverter'
# WEBODT_CONVERTER = 'webodt.converters.openoffice.OpenOfficeODFConverter'
OOFFICE_SERVER = ('127.0.0.1', 2002)

WEBODT_TEMPLATE_PATH = os.path.join(PROJECT_PATH, 'media/templates/')
#WEBODT_TEMPLATE_PATH = '/home/slaviann/work/monitoring/mon/mon/media/templates/'
