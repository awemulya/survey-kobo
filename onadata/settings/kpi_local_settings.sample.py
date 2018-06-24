import os
from settings import *

KOBOCAT_URL = 'http://localhost:8001'
FORGOT_PASSWORD_URL = KOBOCAT_URL + '/accounts/password/reset/'
KOBOCAT_INTERNAL_URL = 'http://localhost:8001'

# KOBOCAT_URL = 'http://192.168.1.17:8001'
# KOBOCAT_INTERNAL_URL = "http://192.168.1.17:8001"
# from kpi.kobo.settings import INSTALLED_APPS
# INSTALLED_APPS += ['debug_toolbar']

# from .settings import INSTALLED_APPS
# INSTALLED_APPS = list(INSTALLED_APPS)
# MIDDLEWARE_CLASSES = list(MIDDLEWARE_CLASSES)
# TEMPLATE_CONTEXT_PROCESSORS = list(TEMPLATE_CONTEXT_PROCESSORS)

# DEBUG_TOOLBAR_CONFIG = {
#     'INTERCEPT_REDIRECTS': True
# }



# DATABASES = {
#     'default': {
#         'ENGINE': 'django.contrib.gis.db.backends.postgis',
#         'NAME': 'v2kpi2',
#         'USER': 'postgres',
#         'PASSWORD': 'password',
#         'HOST': '',
#         'PORT': '',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'testkobo',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': '',
        'PORT': '',
    }
}

MIDDLEWARE_CLASSES = list(MIDDLEWARE_CLASSES)
MIDDLEWARE_CLASSES += ['debug_toolbar.middleware.DebugToolbarMiddleware']

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
os.environ["DJANGO_SECRET_KEY"] = "@25)**hc^rjaiagb4#&q*84hr*uscsxwr-cv#0joiwj$))obyk"
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '@25)**hc^rjaiagb4#&q*84hr*uscsxwr-cv#0joiwj$))obyk')
SESSION_COOKIE_NAME = 'my_cookie'
# SESSION_COOKIE_DOMAIN = "192.168.1.17" #None #'localhost'
SESSION_COOKIE_DOMAIN = 'localhost'

os.environ["ENKETO_VERSION"] = "Express"
ENKETO_URL = os.environ.get('ENKETO_URL', 'http://127.0.0.1:8005/')
ENKETO_SERVER = os.environ.get('ENKETO_URL') or os.environ.get('ENKETO_SERVER', 'http://127.0.0.1:8005/')
ENKETO_SERVER= ENKETO_SERVER + '/' if not ENKETO_SERVER.endswith('/') else ENKETO_SERVER
ENKETO_VERSION= os.environ.get('ENKETO_VERSION', 'Legacy').lower()
#assert ENKETO_VERSION in ['legacy', 'express']
ENKETO_PREVIEW_URI = 'webform/preview' if ENKETO_VERSION == 'legacy' else 'preview'



DEFAULT_DEPLOYMENT_BACKEND = 'kobocat'

BROKER_URL = "redis://localhost:6379/0"

DEBUG = True

# FRONTEND_ENVIRONMENT_DEV_MODE = True

# STATIC_ROOT = os.path.join(ONADATA_DIR, 'admin-static')
#
# STATICFILES_DIRS += (
#         os.path.join(BASE_DIR, 'static'),
#     )

# if FRONTEND_ENVIRONMENT_DEV_MODE:
#     WEBPACK_LOADER = {
#         'DEFAULT': {
#             'CACHE': False,
#             'BUNDLE_DIR_NAME': '/build/',#('/build/' if DEBUG else '/dist/'),
#             'STATS_FILE': os.path.join(BASE_DIR,'webpack', 'webpack-stats-local.json'),
#         }
#     }
# else:
#     WEBPACK_LOADER = {
#         'DEFAULT': {
#             'CACHE': False,
#             'BUNDLE_DIR_NAME': '/dist/',#('/build/' if DEBUG else '/dist/'),
#             'STATS_FILE': os.path.join(BASE_DIR,'webpack', 'webpack-stats.json'),
#         }
#     }
#


CORS_ORIGIN_WHITELIST = (
    'app.fieldsight.org',
    'kc.naxa.com.np',
    'localhost:8001',
    '127.0.0.1:8001',
    'http://192.168.1.111:8001'
)

CORS_URLS_REGEX = r'^/assets/.*$'

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'jsapp/compiled/',
        'POLL_INTERVAL': 0.5,
        'TIMEOUT': 5,
    }
}


# WEBPACK_LOADER = {
#     'DEFAULT': {
#         'BUNDLE_DIR_NAME': 'static/compiled/',
#         'POLL_INTERVAL': 0.5,
#         'TIMEOUT': 5,
#     }
# }