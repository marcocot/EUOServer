from base import *

DEBUG = True

########## TEST SETTINGS

INSTALLED_APPS += (
    'django_jenkins',
    'autofixture',
)

PROJECT_APPS = [
    'backend',
]

JENKINS_TASKS = [
    'django_jenkins.tasks.run_pylint',
    'django_jenkins.tasks.with_coverage',
    'django_jenkins.tasks.run_pep8',
]

########## IN-MEMORY TEST DATABASE
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,

    'formatters': {
        'verbose': {
            'format': '%(levelname)s [%(module)s] %(message)s'
        },

    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'backend': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        },

        'django': {
            'handlers': ['console'],
            'level': 'DEBUG'
        }
    },
}
