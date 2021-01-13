from uuid import uuid4

from django.conf import settings
from django.apps import AppConfig


class DjangoLightAuthConfig(AppConfig):
    name = 'django_light_auth'

    login_path = '/login'
    logout_path = '/logout'
    success_path = '/'

    validate_func = 'django_light_auth.light_auth_validate_func'

    allow_paths = set()

    token = uuid4().hex

    def ready(self):
        value = getattr(settings, 'LIGHT_AUTH_VALIDATE_FUNC', '')
        if value:
            self.validate_func = value
        value = getattr(settings, 'LIGHT_AUTH_LOGIN_PATH', '')
        if value:
            self.login_path = value.rstrip('/')
        value = getattr(settings, 'LIGHT_AUTH_LOGOUT_PATH', '')
        if value:
            self.logout_path = value.rstrip('/')

        self.allow_paths.add(self.login_path)
        self.allow_paths.add(self.logout_path)
