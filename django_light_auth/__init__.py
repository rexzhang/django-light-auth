from .runtimes import (
    do_login,
    do_logout,
    do_validate,

    light_auth_validate_func,

    LightAuthMiddleware,
)
from .views import (
    LoginView,
    LoginForm,

    LogoutView,
)

default_app_config = 'django_light_auth.apps.DjangoLightAuthConfig'

__name__ = 'django-light-auth'
__version__ = '0.2.0'

__author__ = 'Rex Zhang'
__author_email__ = 'rex.zhang@gmail.com'
__licence__ = 'MIT'

__description__ = "Django Lightweight Authentication without models and " \
                  "databases, only depend on the Django's SessionMiddleware."
__project_url__ = 'https://github.com/rexzhang/django-light-auth'
