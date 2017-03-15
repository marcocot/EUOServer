"""Production settings and globals."""

from base import *

########## HOST CONFIGURATION
# See: https://docs.djangoproject.com/en/1.5/releases/1.5/#allowed-hosts-required-in-production
ALLOWED_HOSTS = [
    'devncode.it',
    'euoserver.devncode.it',
    'localhost',
    '127.0.0.1',
]
########## END HOST CONFIGURATION

########## MEDIA CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = normpath(join(SITE_ROOT, '../media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'
########## END MEDIA CONFIGURATION

########## STATIC FILE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = normpath(join(SITE_ROOT, '../assets'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = None
EMAIL_PORT = 25
EMAIL_SUBJECT_PREFIX = '[%s] ' % SITE_NAME
EMAIL_USE_TLS = False
SERVER_EMAIL = 'marco.cotrufo@devncode.it'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': SITE_ROOT + "/../logs/django.log",
            'maxBytes': 50000,
            'backupCount': 10,
            'formatter': 'standard',
        },
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'backend': {
            'handlers': ['logfile', 'console'],
            'handlers': ['logfile'],
            'level': 'DEBUG',
            'propagate': True
        },
        'euoserver': {
            'handlers': ['logfile', 'console'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django': {
            'handlers': ['logfile', 'console'],
            'level': 'INFO',
            'propagate': True
        }
    },
}

SECRET_KEY = env('SECRET_KEY')