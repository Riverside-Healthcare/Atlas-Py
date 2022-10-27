"""
Django settings for atlas project.

Generated by 'django-admin startproject' using Django 3.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import contextlib
import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import saml2
import saml2.saml

try:
    import tomllib
except ImportError:
    import tomli as tomllib  # type: ignore

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
BASE_URL = "https://atlas.bi/"
SAML_CONFIG = {
    "xmlsec_binary": "/usr/bin/xmlsec1",
    "entityid": BASE_URL + "saml2/metadata/",
    "allow_unknown_attributes": True,
    "service": {
        "sp": {
            "name": "Atlas of Information Management SP",
            "name_id_format": saml2.saml.NAMEID_FORMAT_PERSISTENT,
            "allow_unsolicited": True,
            "endpoints": {
                "assertion_consumer_service": [
                    (BASE_URL + "saml2/acs/", saml2.BINDING_HTTP_POST),
                ],
                "single_logout_service": [
                    (BASE_URL + "saml2/ls/", saml2.BINDING_HTTP_REDIRECT),
                    (BASE_URL + "saml2/ls/post/", saml2.BINDING_HTTP_POST),
                ],
            },
            "force_authn": False,
            "name_id_format_allow_create": True,
            "authn_requests_signed": False,
            "logout_requests_signed": True,
            "want_assertions_signed": True,
            "want_response_signed": False,
        },
    },
    "metadata": {
        "remote": [
            {
                "url": "https://rhcfs.atlas.bi/FederationMetadata/2007-06/FederationMetadata.XML",
                "disable_ssl_certificate_validation": True,
            },
        ],
    },
    "debug": 1,
    "key_file": str(BASE_DIR.parent / "publish/cert.key"),  # private part
    "cert_file": str(BASE_DIR.parent / "publish/cert.crt"),  # public part
    "encryption_keypairs": [
        {
            "key_file": str(BASE_DIR.parent / "publish/cert.key"),  # private part
            "cert_file": str(BASE_DIR.parent / "publish/cert.crt"),  # public part
        }
    ],
    "contact_person": [
        {
            "given_name": "Christopher",
            "sur_name": "Pickering",
            "company": "Riverside Healthcare",
            "email_address": "",
            "contact_type": "technical",
        },
    ],
    "organization": {
        "name": [("Riverside Healthcare", "en")],
        "display_name": [("Riverside Healthcare", "en")],
        "url": [("http://atlas", "en")],
    },
}

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "cbLKvrnTXB8l0iVzo+PhwXp75HUqByiUyNoXAAt/gfPLlAYxkJlUWUz8itbHYCYkj9dOS9L66PmiWbGYn7rj1w==",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
DEMO = False

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
]

INTERNAL_IPS = [
    "127.0.0.1",
    "localhost",
]

SESSION_ENGINE = "redis_sessions.session"

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)
REDIS_URL = os.environ.get("REDIS_URL", "redis://127.0.0.1:6379")

SESSION_REDIS = {
    "host": REDIS_HOST,
    "port": REDIS_PORT,
    "db": 0,
    "prefix": "atlas_session",
    "socket_timeout": 1,
    "retry_on_timeout": False,
}


INSTALLED_APPS = [
    # "django.contrib.admin",
    # django stuff
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Nice django add-ons
    "compressor",
    "djangosaml2",
    "mathfilters",
    "django_celery_results",
    "django_celery_beat",
    "fullurl",
    # Atlas specific
    "index.apps.IndexConfig",
    "mail.apps.MailConfig",
    "analytics.apps.AnalyticsConfig",
    "report.apps.ReportConfig",
    "search.apps.SearchConfig",
    "term.apps.TermConfig",
    "initiative.apps.InitiativeConfig",
    "collection.apps.CollectionConfig",
    "user.apps.UserConfig",
    "etl.apps.EtlConfig",
    "settings.apps.SettingsConfig",
    "group.apps.GroupConfig",
    "sketch.apps.SketchConfig",
    "task.apps.TaskConfig",
]

MIDDLEWARE = [
    "django.middleware.cache.UpdateCacheMiddleware",  # for caching
    "compression_middleware.middleware.CompressionMiddleware",
    "htmlmin.middleware.HtmlMinifyMiddleware",  # for htmlmin
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.cache.FetchFromCacheMiddleware",  # for caching
    "htmlmin.middleware.MarkRequestMiddleware",  # for htmlmin
    "djangosaml2.middleware.SamlSessionMiddleware",
]

AUTHENTICATION_BACKENDS: Tuple[str, ...] = (
    "django.contrib.auth.backends.ModelBackend",
    "djangosaml2.backends.Saml2Backend",
)

ROOT_URLCONF = "atlas.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # "atlas.context_processors.settings",
                "atlas.context_processors.user",
                "django_settings_export.settings_export",
            ],
            "libraries": {
                "markdown": "atlas.templatetags.markdown",
                "dates": "atlas.templatetags.dates",
                "helpers": "atlas.templatetags.helpers",
                "atlas_static": "atlas.templatetags.static",
            },
            "debug": DEBUG,
        },
    },
]

WSGI_APPLICATION = "atlas.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES: Dict[Any, Any] = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "atlas",
        "HOST": "postgres",
        "USER": "postgres",
        "PASSWORD": "",
    },
}

# routers used to divert some traffic to another db (sql server)
DATABASE_ROUTERS = ["index.routers.IndexRouter"]


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_URL,
    }
}
CACHE_MIDDLEWARE_ALIAS = "default"
CACHE_MIDDLEWARE_SECONDS = 20
CACHE_MIDDLEWARE_KEY_PREFIX = ""


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/Chicago"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

DEFAULT_ROOT = BASE_DIR / "defaults"

COMPRESS_ROOT = BASE_DIR / "static"
COMPRESS_CSS_HASHING_METHOD = "content"

COMPRESS_FILTERS = {
    "css": [
        "compressor.filters.css_default.CssAbsoluteFilter",
        "compressor.filters.cssmin.rCSSMinFilter",
    ],
    "js": [
        "compressor.filters.jsmin.JSMinFilter",
    ],
}

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)

COMPRESS_PRECOMPILERS = (
    # ("text/x-scss", "django_libsass.SassCompiler"),
    ("text/x-scss", "$(npm run postcss {infile} -o {outfile} --verbose)"),
    #  ("text/javascript", "npm run babel {infile} -- --out-file {outfile}"),
    # ("test/css", "npm run postcss {infile} -o {outfile} --verbose"),
)

LIBSASS_OUTPUT_STYLE = "compressed"

HTML_MINIFY = True
KEEP_COMMENTS_ON_MINIFYING = False

LOGIN_URL = "/saml2/login/"
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SAML_ALLOWED_HOSTS = ALLOWED_HOSTS
AUTH_USER_MODEL = "index.Users"
SILENCED_SYSTEM_CHECKS = ["auth.W004"]  # disable username warning
SAML_IGNORE_LOGOUT_ERRORS = True
SAML_SESSION_COOKIE_NAME = "saml_session"
SAML_USE_NAME_ID_AS_USERNAME = False
SAML_DJANGO_USER_MAIN_ATTRIBUTE = "email"
SAML_DJANGO_USER_MAIN_ATTRIBUTE_LOOKUP = "__iexact"
SAML_CREATE_UNKNOWN_USER = True
SAML_ATTRIBUTE_MAPPING = {
    "emailAddress": (
        "email",
        "username",
    ),
}

ORG_NAME = "Riverside Healthcare"

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

SOLR_URL = "http://localhost:8983/solr/atlas/"
SOLR_LOOKUP_URL = "http://localhost:8983/solr/atlas_lookups/"

# Celery configuration
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = "django-db"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
DJANGO_CELERY_BEAT_TZ_AWARE = True
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
CELERY_RESULT_EXTENDED = True
CELERY_IMPORTS = ["etl.tasks.search"]

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
        "level": "WARNING",
    },
}


def find_project_root(src: Path) -> Path:
    """Attempt to get the project root."""
    for directory in [src, *src.resolve().parents]:

        if (directory / "pyproject.toml").is_file():
            return directory

    # pylint: disable=W0631
    return directory


def find_pyproject(root: Path) -> Optional[Path]:
    """Search upstream for a pyproject.toml file."""
    pyproject = root / "pyproject.toml"

    if pyproject.is_file():
        return pyproject

    return None


pyproject_file = find_pyproject(find_project_root(Path(__file__)))

if pyproject_file:
    content = tomllib.load(pyproject_file.open("rb"))
    try:
        VERSION = content["tool"]["poetry"]["version"]  # type: ignore
    except KeyError:
        VERSION = ""
        logging.info("No pyproject.toml found.")


DOMAIN = "example.com"
FOOTER = {
    "SUBTITLE": "Atlas was created by the Riverside Healthcare Analytics team.",
    "LINKS": {
        "Status": {
            "Epic": "https://bigbrother.riversidehealthcare.net/status/epic",
            "Atlas": "https://bigbrother.riversidehealthcare.net/status/atlas",
        }
    },
}
SITE_MESSAGE = "Welcome to Atlas"
LOGO = "img/thinking-face-text-266x80.png"

ENABLE_INITIATIVES = True
ENABLE_REQUEST_ACCESS = True
ENABLE_SHARING = True
ENABLE_TERMS = True
ENABLE_USER_PROFILES = True
ENABLE_BREADCRUMBS = True

EMAIL_HOST = ""
EMAIL_PORT = 25
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False
EMAIL_HOST_USER = None
EMAIL_HOST_PASSWORD = None
EMAIL_SENDER_NAME = f"Atlas | {ORG_NAME} Analytics"
EMAIL_SENDER_EMAIL = "me@example.com"
EMAIL_DEFAULT_REPLY_ADDRESS = "me@example.com"

# import custom overrides
with contextlib.suppress(ImportError):
    from .settings_cust import *

SETTINGS_EXPORT = [
    "ORG_NAME",
    "DEMO",
    "FOOTER",
    "VERSION",
    "SITE_MESSAGE",
    "ENABLE_INITIATIVES",
    "ENABLE_REQUEST_ACCESS",
    "ENABLE_SHARING",
    "ENABLE_TERMS",
    "ENABLE_USER_PROFILES",
    "ENABLE_BREADCRUMBS",
]

SAFE_HTML_TAGS = [
    "a",
    "abbr",
    "acronym",
    "address",
    "area",
    "article",
    "aside",
    "audio",
    "b",
    "big",
    "blockquote",
    "br",
    "button",
    "canvas",
    "caption",
    "center",
    "cite",
    "code",
    "col",
    "colgroup",
    "command",
    "datagrid",
    "datalist",
    "dd",
    "del",
    "details",
    "dfn",
    "dialog",
    "dir",
    "div",
    "dl",
    "dt",
    "em",
    "event-source",
    "fieldset",
    "figcaption",
    "figure",
    "footer",
    "font",
    "form",
    "header",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "hr",
    "i",
    "img",
    "input",
    "ins",
    "keygen",
    "kbd",
    "label",
    "legend",
    "li",
    "m",
    "map",
    "menu",
    "meter",
    "multicol",
    "nav",
    "nextid",
    "ol",
    "output",
    "optgroup",
    "option",
    "p",
    "pre",
    "progress",
    "q",
    "s",
    "samp",
    "section",
    "select",
    "small",
    "sound",
    "source",
    "spacer",
    "span",
    "strike",
    "strong",
    "sub",
    "sup",
    "table",
    "tbody",
    "td",
    "textarea",
    "time",
    "tfoot",
    "th",
    "thead",
    "tr",
    "tt",
    "u",
    "ul",
    "var",
    "video",
]
