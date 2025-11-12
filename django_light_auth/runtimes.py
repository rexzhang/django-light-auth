import logging
from collections.abc import Callable
from typing import Any

from django.apps import apps
from django.http import HttpRequest, HttpResponseRedirect

logger = logging.getLogger(__file__)

TOKEN_KEY = "light_auth_token"


def _get_session_from_request(request: HttpRequest):
    try:
        session = request.__getattribute__("session")
    except AttributeError:
        raise Exception(
            "Missed django.contrib.sessions.middleware.SessionMiddleware, "
            "django-light-auth depend it."
        )
    return session


def do_login(request: HttpRequest) -> str:
    session = _get_session_from_request(request)
    session[TOKEN_KEY] = apps.get_app_config("django_light_auth").token
    expiry = apps.get_app_config("django_light_auth").expiry
    if expiry is not None:
        # https://docs.djangoproject.com/en/3.1/topics/http/sessions/
        # "If value is None,
        # the session reverts to using the global session expiry policy."
        session.set_expiry(apps.get_app_config("django_light_auth").expiry)

    return apps.get_app_config("django_light_auth").success_path


def do_logout(request: HttpRequest) -> str:
    session = _get_session_from_request(request)
    session[TOKEN_KEY] = False

    return apps.get_app_config("django_light_auth").login_path


def _import_func(func_name: str, father_model=None) -> Callable | None:
    try:
        index = func_name.find(".")
        if index == -1:
            func = getattr(father_model, func_name[index + 1 :])
            return func

        else:
            if father_model is None:
                module = __import__(func_name[:index])

            else:
                module = getattr(father_model, func_name[:index])

            return _import_func(func_name[index + 1 :], module)

    except (ImportError, AttributeError, ValueError) as e:
        logger.error(e)
        logger.error(f"func_name: {func_name}, father_model:{father_model}")
        return None


def do_validate(data: dict[str, Any]) -> bool:
    func_name = apps.get_app_config("django_light_auth").validate_func

    func = _import_func(func_name)
    if func is None:
        raise ImportError(f"Can import: {func_name}")

    if func(data):
        return True

    return False


def light_auth_validate_func(data: dict[str, Any]) -> bool:
    """demo for setting.LIGHT_AUTH_VALIDATE_FUNC"""
    if data.get("username", None) == data.get("password", None):
        return True

    return False


def validate_request(request: HttpRequest) -> bool:
    path = request.path.rstrip("/")
    if path in apps.get_app_config("django_light_auth").allow_paths:
        return True

    session = _get_session_from_request(request)
    token = session.get(TOKEN_KEY, "")
    if token == apps.get_app_config("django_light_auth").token:
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
                apps.get_app_config("django_light_auth").login_path
            )

        return response
