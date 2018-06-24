import os

os.environ["DJANGO_SECRET_KEY"] = "@25)**hc^rjaiagb4#&q*84hr*uscsxwr-cv#0joiwj$))obyk"
os.environ["KOBOCAT_MONGO_HOST"] = "localhost"
os.environ["CSRF_COOKIE_DOMAIN"] = "localhost"

from onadata.settings.kc_environ import *
# TESTING_MODE = True
# ANGULAR_URL = '/ng/'
# ANGULAR_ROOT = os.path.join(BASE_DIR, 'ng/')
CORS_ORIGIN_ALLOW_ALL = True
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

INSTALLED_APPS = list(INSTALLED_APPS)

INSTALLED_APPS += ['onadata.apps.office',]
INSTALLED_APPS += ['debug_toolbar',]
# MIDDLEWARE_CLASSES = list(MIDDLEWARE_CLASSES)
# MIDDLEWARE_CLASSES += ['debug_toolbar.middleware.DebugToolbarMiddleware']
# INSTALLED_APPS += ['debug_toolbar', 'channels', 'fcm']
# INSTALLED_APPS += ['debug_toolbar', 'fcm', 'webpack_loader']

# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "asgi_redis.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [("localhost", 6379)],
#         },
#         "ROUTING": "onadata.apps.fieldsight.routing.channel_routing",
#     },
# }

WEBSOCKET_URL = "localhost"

WEBSOCKET_PORT = "8001"

KPI_LOGOUT_URL = 'http://localhost:8000/accounts/logout/'


FCM_APIKEY = "AAAA8R_cP8A:APA91bH6r8ufI3KOL2h-1CIm7fswvp88QRYgARtvP50y8zIouvu-8JsJ1Tmv62MFA9Kn1dhm7u0kxmXy" \
             "cLiQJfhvN81ItHCWmgWHUNGTwX54Ma3RN6UkILRwa9CR0qO6PHnrQFSjGYOy5vHfQ_w31J7Rk134LrsTUQ"

FCM_MAX_RECIPIENTS = 1000

SERIALIZATION_MODULES = {
        "custom_geojson": "onadata.apps.fieldsight.serializers.GeoJSONSerializer",
}


SEND_ACTIVATION_EMAIL = True
ACCOUNT_ACTIVATION_DAYS = 30
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'app.fieldsight@gmail.com'
SERVER_EMAIL = 'app.fieldsight@gmail.com'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'app.fieldsight@gmail.com'
EMAIL_HOST_PASSWORD = '@app@fieldsight111'


CORS_ORIGIN_WHITELIST = (
    'dev.ona.io',
    'google.com',
    'app.fieldsight.org',
    'kpi.fieldsight.org',
    'bcss.com.np.com',
    'kc.bcss.com.np',
    'localhost:8001',
    '127.0.0.1:8000'
)

TIME_ZONE = 'Asia/Kathmandu'

from onadata.settings.common import REST_FRAMEWORK
REST_FRAMEWORK.update({'DEFAULT_PERMISSION_CLASSES':['rest_framework.permissions.IsAuthenticated',]})


# DEBUG_TOOLBAR_CONFIG = {
#     'INTERCEPT_REDIRECTS': True
# }

FILE_UPLOAD_HANDLERS = ("django_excel.ExcelMemoryFileUploadHandler",
                        "django_excel.TemporaryExcelFileUploadHandler")

# DEBUG = False

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '@25)**hc^rjaiagb4#&q*84hr*uscsxwr-cv#0joiwj$))obyk')
SESSION_COOKIE_NAME = 'my_cookie'
# SESSION_COOKIE_DOMAIN = '192.168.1.17'
# SESSION_COOKIE_DOMAIN = None
DEFAULT_DEPLOYMENT_BACKEND = 'localhost'



BROKER_BACKEND = "redis"
CELERY_RESULT_BACKEND = "redis"  # telling Celery to report results to RabbitMQ
# CELERY_ALWAYS_EAGER = True
BROKER_URL = 'redis://localhost:6379'

ADMINS = [('Amulya', 'awemulya@gmail.com'), ('AruVan', 'mearunbhandari@gmail.com')]

# CELERY_IMPORTS = ('tasks','onadata.apps.fieldsight.tasks')

# if testing mode
os.environ["ENKETO_VERSION"] = "Express"
ENKETO_URL = os.environ.get('ENKETO_URL', 'http://127.0.0.1:8005/')
ENKETO_SERVER = os.environ.get('ENKETO_URL') or os.environ.get('ENKETO_SERVER', 'http://127.0.0.1:8005/')
ENKETO_SERVER= ENKETO_SERVER + '/' if not ENKETO_SERVER.endswith('/') else ENKETO_SERVER
ENKETO_VERSION= os.environ.get('ENKETO_VERSION', 'Legacy').lower()
#assert ENKETO_VERSION in ['legacy', 'express']
ENKETO_PREVIEW_URI = 'webform/preview' if ENKETO_VERSION == 'legacy' else 'preview'
FRONTEND_ENVIRONMENT_DEV_MODE = True

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
