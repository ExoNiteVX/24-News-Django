import os
from pathlib import Path
from dotenv import load_dotenv
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = ''

DEBUG = True

ALLOWED_HOSTS = []
SITE_ID = 1

INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.sites",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "django_ratelimit",

    "app.apps.AppConfig"
]

LOGIN_URL =  'login'
LOGIN_REDIRECT_URL = '/profile'
LOGOUT_REDIRECT_URL = 'login'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

UNFOLD = {
    "SITE_TITLE": "24 News Admin",
    "SITE_HEADER": "24 News Portal",
    "SITE_URL": "/",
    "SITE_SYMBOL": "newspaper",
    "THEME": "dark",
    "DARK_MODE": True,
    "DARK_MODE_ENABLED": True,
    "COLOR_SCHEME": ["dark"],
    
    "STYLES": [
        lambda request: "admin/css/dark_mode.css?v=3",
    ],
    
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": _("Dashboard"),
                "icon": "dashboard",
                "link": reverse_lazy("admin:index"),
            },
            {
                "separator": True,
                "title": _("Content"),
            },
            {
                "title": _("News"),
                "icon": "article",
                "link": reverse_lazy("admin:app_news_changelist"),
            },
            {
                "title": _("Single Pages"),
                "icon": "description",
                "link": reverse_lazy("admin:app_singlepage_changelist"),
            },
            {
                "title": _("Comments"),
                "icon": "comment",
                "link": reverse_lazy("admin:app_comment_changelist"),
            },
        ],
        "app_list_template": """
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            {% for app in app_list %}
            <div class="bg-base-900 border border-base-800 rounded-lg p-6 hover:border-blue-500/50 transition-colors">
                <div class="flex items-center gap-4 mb-4">
                    <div class="w-12 h-12 rounded-lg bg-blue-500/20 flex items-center justify-center">
                        <span class="text-blue-500 text-xl font-bold">{{ app.name|first|upper }}</span>
                    </div>
                    <div>
                        <h3 class="font-semibold text-lg text-font-important">{{ app.name }}</h3>
                        <p class="text-sm text-font-subtle">{{ app.models|length }} models</p>
                    </div>
                </div>
                <div class="space-y-2">
                    {% for model in app.models %}
                    <a href="{{ model.admin_url }}" class="flex items-center justify-between px-4 py-3 rounded hover:bg-base-800 text-sm text-font-default transition-colors">
                        <span>{{ model.name }}</span>
                        <svg class="w-4 h-4 text-font-subtle" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                        </svg>
                    </a>
                    {% endfor %}
                </div>
            </div>
            {% endfor %}
        </div>
        """,
    },
    
    "USER": {
        "link": reverse_lazy("admin:app_userprofile_changelist"),
    },
    
    "COLORS": {
        "primary": {
            "50": "250 250 250",
            "100": "244 244 245",
            "200": "228 228 231",
            "300": "212 212 216",
            "400": "161 161 170",
            "500": "113 113 122",
            "600": "82 82 91",
            "700": "63 63 70",
            "800": "39 39 42",
            "900": "24 24 27",
            "950": "9 9 11",
        },
        "font": {
            "subtle": "161 161 170",
            "default": "212 212 216",
            "important": "250 250 250",
        },
    },
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'

LANGUAGES = [
    ('en', 'English'),
    ('de', 'Deutsch'),
    ('fr', 'French'),
    ('es', 'Spanish'),
    ('uz', 'Uzbek'),
    ('ru', 'Russian'),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale'
]
USE_I18N = True

USE_TZ = True

SITE_URL = "http://127.0.0.1:8000"

# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

load_dotenv(os.path.join(BASE_DIR, '.env'))

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER


ACCOUNT_SIGNUP_FIELDS = ['email', 'password1', 'password2']


TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')