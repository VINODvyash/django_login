"""
Django settings for config project - Production Configuration
Extends base.py with production-specific settings and security hardening.
"""

from .base import *  # noqa
import logging
from decouple import config

# ═════════════════════════════════════════════════════════════════════════════
# DEBUG & SECURITY
# ═════════════════════════════════════════════════════════════════════════════

DEBUG = False
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv()).split(',')

# ═════════════════════════════════════════════════════════════════════════════
# DATABASE - PRODUCTION (PostgreSQL recommended)
# ═════════════════════════════════════════════════════════════════════════════

DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE', default='django.db.backends.postgresql'),
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default='5432'),
        'ATOMIC_REQUESTS': True,
        'CONN_MAX_AGE': 600,
    }
}

# ═════════════════════════════════════════════════════════════════════════════
# REST FRAMEWORK - PRODUCTION
# ═════════════════════════════════════════════════════════════════════════════

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
    'rest_framework.renderers.JSONRenderer',
]

REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'] = [
    'rest_framework.permissions.IsAuthenticated',
]

REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'] = {
    'anon': '50/hour',
    'user': '500/hour',
}

# ═════════════════════════════════════════════════════════════════════════════
# SSL/HTTPS SECURITY
# ═════════════════════════════════════════════════════════════════════════════

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# ═════════════════════════════════════════════════════════════════════════════
# ALLOWED HOSTS & TRUSTED ORIGINS
# ═════════════════════════════════════════════════════════════════════════════

CSRF_TRUSTED_ORIGINS = config(
    'CSRF_TRUSTED_ORIGINS',
    default='https://example.com',
    cast=Csv()
)

# ═════════════════════════════════════════════════════════════════════════════
# EMAIL CONFIGURATION
# ═════════════════════════════════════════════════════════════════════════════

EMAIL_BACKEND = config(
    'EMAIL_BACKEND',
    default='django.core.mail.backends.smtp.EmailBackend'
)
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@example.com')

# ═════════════════════════════════════════════════════════════════════════════
# CACHE - PRODUCTION (Redis recommended)
# ═════════════════════════════════════════════════════════════════════════════

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': config('REDIS_URL', default='redis://127.0.0.1:6379/0'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# ═════════════════════════════════════════════════════════════════════════════
# LOGGING - PRODUCTION
# ═════════════════════════════════════════════════════════════════════════════

LOGGING['handlers']['file'] = {
    'class': 'logging.handlers.RotatingFileHandler',
    'filename': BASE_DIR / 'logs' / 'django.log',
    'maxBytes': 1024 * 1024 * 15,  # 15MB
    'backupCount': 10,
    'formatter': 'verbose',
}

LOGGING['handlers']['file-errors'] = {
    'class': 'logging.handlers.RotatingFileHandler',
    'filename': BASE_DIR / 'logs' / 'django-errors.log',
    'maxBytes': 1024 * 1024 * 15,
    'backupCount': 10,
    'formatter': 'verbose',
    'level': 'ERROR',
}

LOGGING['root']['handlers'] = ['file', 'file-errors']
LOGGING['loggers']['django']['handlers'] = ['file', 'file-errors']

# ═════════════════════════════════════════════════════════════════════════════
# SENTRY ERROR TRACKING (Optional)
# ═════════════════════════════════════════════════════════════════════════════

SENTRY_DSN = config('SENTRY_DSN', default='')
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.1,
        send_default_pii=False,
    )

# ═════════════════════════════════════════════════════════════════════════════
# STATIC FILES - PRODUCTION (Using WhiteNoise or CDN)
# ═════════════════════════════════════════════════════════════════════════════

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ═════════════════════════════════════════════════════════════════════════════
# CONTENT SECURITY POLICY
# ═════════════════════════════════════════════════════════════════════════════

SECURE_CONTENT_SECURITY_POLICY = {
    "default-src": ("'self'",),
    "script-src": ("'self'", "cdn.example.com"),
    "style-src": ("'self'", "'unsafe-inline'"),
    "img-src": ("'self'", "data:", "https:"),
    "font-src": ("'self'", "data:"),
}

# ═════════════════════════════════════════════════════════════════════════════
# ADMIN SECURITY
# ═════════════════════════════════════════════════════════════════════════════

ADMIN_URL = config('ADMIN_URL', default='admin/')

# ═════════════════════════════════════════════════════════════════════════════
# SESSION SECURITY
# ═════════════════════════════════════════════════════════════════════════════

SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_AGE = 86400  # 24 hours
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# ═════════════════════════════════════════════════════════════════════════════
# MIDDLEWARE - ADD FOR PRODUCTION
# ═════════════════════════════════════════════════════════════════════════════

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
] + MIDDLEWARE
