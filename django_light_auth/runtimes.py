import logging
from typing import Dict, Any, Optional, Callable

from django.apps import apps
from django.http import HttpRequest, HttpResponseRedirect

logger = logging.getLogger(__file__)

TOKEN_KEY = 'light_auth_token'


def do_login(request: HttpRequest) -> str:
    request.session[TOKEN_KEY] = apps.get_app_config(
        'django_light_auth'
    ).token

    return apps.get_app_config('django_light_auth').success_path


def do_logout(request: HttpRequest) -> str:
    request.session[TOKEN_KEY] = False

    return apps.get_app_config('django_light_auth').login_path


def _import_func(func_name: str, father_model=None) -> Optional[Callable]:
    try:
        index = func_name.find('.')
        if index == -1:
            func = getattr(father_model, func_name[index + 1:])
            return func

        else:
            if father_model is None:
                module = __import__(func_name[:index])

            else:
                module = getattr(father_model, func_name[:index])

            return _import_func(func_name[index + 1:], module)

    except (ImportError, AttributeError, ValueError) as e:
        logger.error(e)
        logger.error('func_name: {}, father_model:{}'.format(
            func_name, father_model
        ))
        return None


def do_validate(data: Dict[str, Any]) -> bool:
    func_name = apps.get_app_config('django_light_auth').validate_func

    func = _import_func(func_name)
    if func is None:
        raise ImportError('Can import: {}'.format(func_name))

    if func(data):
        return True

    return False


def light_auth_validate_func(data: Dict[str, Any]) -> bool:
    """demo for setting.LIGHT_AUTH_VALIDATE_FUNC"""
    if data.get('username', None) == data.get('password', None):
        return True

    return False


def validate_request(request: HttpRequest) -> bool:
    path = request.path.rstrip('/')
    if path in apps.get_app_config('django_light_auth').allow_paths:
        return True

    token = request.session.get(TOKEN_KEY, '')
    if token == apps.get_app_config('django_light_auth').token:
        return True

    return False


class LightAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request: HttpRequest):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        if not validate_request(request):
            return HttpResponseRedirect(
                apps.get_app_config('django_light_auth').login_path
            )

        return response
