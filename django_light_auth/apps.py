from datetime import datetime, timedelta
from uuid import uuid4

from django.apps import AppConfig
from django.conf import settings


class DjangoLightAuthConfig(AppConfig):
    name = "django_light_auth"
    default = True

    login_path = "/login"
    logout_path = "/logout"
    success_path = "/"

    validate_func = "django_light_auth.light_auth_validate_func"

    allow_paths = set()

    token = uuid4().hex
    # https://docs.djangoproject.com/en/3.1/topics/http/sessions/
    expiry: None | int | datetime | timedelta = 3600  # 1 hour

    def ready(self):
        # func
        value = getattr(settings, "LIGHT_AUTH_VALIDATE_FUNC", "")
        if value:
            self.validate_func = value

        # path
        value = getattr(settings, "LIGHT_AUTH_LOGIN_PATH", "")
        if value:
            self.login_path = value.rstrip("/")
        value = getattr(settings, "LIGHT_AUTH_LOGOUT_PATH", "")
        if value:
            self.logout_path = value.rstrip("/")

        self.allow_paths.add(self.login_path)
        self.allow_paths.add(self.logout_path)

        # expiry
        value = getattr(settings, "LIGHT_AUTH_EXPIRY", None)
        if value is None:
            # https://docs.djangoproject.com/en/3.1/topics/http/sessions/
            # "If value is None,
            # the session reverts to using the global session expiry policy."
            self.expiry = None
        elif isinstance(value, int) and value >= 0:
            self.expiry = value
        elif isinstance(value, (datetime, timedelta)):
            self.expiry = value
