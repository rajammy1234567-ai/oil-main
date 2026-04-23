import os
from pathlib import Path
import environ
import importlib.util
import dj_database_url

# Initialize Cloudinary (optional but good practice)
import cloudinary
import cloudinary.uploader
import cloudinary.api

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()

# Read .env files
read_any = False
root_env = BASE_DIR / '.env'
alt_env = BASE_DIR / 'cattle' / '.env'

if root_env.exists():
    environ.Env.read_env(str(root_env))
    read_any = True
if alt_env.exists():
    environ.Env.read_env(str(alt_env))
    read_any = True

if not read_any:
    try:
        environ.Env.read_env()
    except Exception:
        pass

SECRET_KEY = env('SECRET_KEY', default='dev-secret')
DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = [
    'karyor.com',
    'www.karyor.com',
    'karyor-com.onrender.com',
    'cattle-1.onrender.com',
]
# Add hosts from environment variable (Render)
env_hosts = env.list('ALLOWED_HOSTS', default=[])
ALLOWED_HOSTS.extend(env_hosts)

# Remove duplicates
ALLOWED_HOSTS = list(set(ALLOWED_HOSTS))

CSRF_TRUSTED_ORIGINS = [
    "https://karyor.com",
    "https://www.karyor.com",
    "https://karyor-com.onrender.com",
    "https://cattle-1.onrender.com",
]

# ========== CLOUDINARY CONFIGURATION ==========
# Confirmed working credentials
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env('CLOUDINARY_CLOUD_NAME', default='dhjnveoxf'),
    'API_KEY': env('CLOUDINARY_API_KEY', default='445972572321883'),
    'API_SECRET': env('CLOUDINARY_API_SECRET', default='6h-5srcDUQ8-4dkx5BxHVGp40As'),
    'SECURE': True,
}

# Configure Cloudinary SDK
cloudinary.config(
    cloud_name=CLOUDINARY_STORAGE['CLOUD_NAME'],
    api_key=CLOUDINARY_STORAGE['API_KEY'],
    api_secret=CLOUDINARY_STORAGE['API_SECRET'],
    secure=True
)

# Use Cloudinary for media files
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# ========== INSTALLED APPS ==========
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Cloudinary apps (MUST be in this order!)
    'cloudinary_storage',  # This FIRST
    'cloudinary',          # This SECOND
    
    # Your apps
    'rest_framework',
    'social_django',
    'accounts',
    'products',
    'videos',
    'orders',
    'payments',
    'notifications',
    'cms',
    'website',
    'whatsapp',
]

# Add Jazzmin if available
if importlib.util.find_spec('jazzmin') is not None:
    INSTALLED_APPS.insert(0, 'jazzmin')

# ========== MIDDLEWARE ==========
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cattle.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'cattle.wsgi.application'

# ========== DATABASE ==========
DATABASES = {
    'default': dj_database_url.config(
        default=env('DATABASE_URL', default='sqlite:///db.sqlite3'),
        conn_max_age=600
    )
}

AUTH_PASSWORD_VALIDATORS = []

# ========== AUTHENTICATION ==========
AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY', default='')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET', default='')
SOCIAL_AUTH_URL_NAMESPACE = 'social'

SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
]

# HTTPS settings
SOCIAL_AUTH_REDIRECT_IS_HTTPS = not DEBUG
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
if not DEBUG:
    SECURE_HSTS_SECONDS = 31536000 # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# ========== INTERNATIONALIZATION ==========
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_L10N = True
USE_TZ = True
 
# ========== STATIC FILES ==========
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
WHITENOISE_MANIFEST_STRICT = False

# ========== MEDIA FILES (Cloudinary) ==========
# Cloudinary will handle media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ========== RAZORPAY ==========
RAZORPAY_KEY_ID = env('RAZORPAY_KEY_ID', default='')
RAZORPAY_KEY_SECRET = env('RAZORPAY_KEY_SECRET', default='')
RAZORPAY_WEBHOOK_SECRET = env('RAZORPAY_WEBHOOK_SECRET', default='')

# ========== JAZZMIN ==========
JAZZMIN_SETTINGS = {
    "site_title": "CattleCart Admin",
    "site_header": "CattleCart",
    "site_brand": "CattleCart",
}