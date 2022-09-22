"""Atlas Settings for Test."""

import os

from .base import *


class DisableMigrations:
    """Disable migrations to force a fresh db load."""

    def __contains__(self, item):
        """Return true for all keys."""
        return True

    def __getitem__(self, item):
        """Return none for all values."""
        return None


AUTHENTICATION_BACKENDS = ("atlas.no_pass_auth.Backend",)

LOGIN_URL = "/accounts/login/"

"""
docker run --name postgresql-container -p 5432:5432 -e POSTGRES_HOST_AUTH_METHOD=trust -d postgres
"""

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "atlas"),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "USER": "postgres",
        "PASSWORD": os.environ.get("PGPASSWORD", ""),
    },
}

TESTING = True
LOGIN_REDIRECT_URL = "/"

COMPRESS_ENABLED = False

DATABASE_ROUTERS: list = []

# make celery tasks run as blocking
CELERY_BROKER_URL = "memory://"
CELERY_RESULT_BACKEND = "cache+memory://"
CELERY_ALWAYS_EAGER = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "ERROR",
    },
}

# pretend there are no migrations. By default the tests will create a database that is based
# on the latest migrations. Since we are not doing any migrations on the psql db (app is using
# mssql db in production/dev), we can ignore migrations for tests and just create a db based
# on the models.py file.
MIGRATION_MODULES = DisableMigrations()

# import custom overrides
try:
    from .test_cust import *
except ImportError:
    pass
