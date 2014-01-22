from base import *

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
