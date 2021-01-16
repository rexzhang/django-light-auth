# django-light-auth

[![](https://img.shields.io/pypi/v/django-light-auth.svg)](https://pypi.org/project/django-light-auth/)
[![](https://img.shields.io/pypi/pyversions/django-light-auth.svg)](https://pypi.org/project/django-light-auth/)
[![](https://img.shields.io/pypi/dm/django-light-auth.svg)](https://pypi.org/project/django-light-auth/)

> Django lightweight authentication without models and databases, only depend SessionMiddleware

# Install

```shell
pip3 install -U django-light-auth
```

# Basic Usage

## `settings.py`

```python
INSTALLED_APPS = [
    # ...

    'django_light_auth',

    # ...
]

MIDDLEWARE = [
    # ...

    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_light_auth.LightAuthMiddleware'

    # ...
]

LIGHT_AUTH_VALIDATE_FUNC = 'your_app.auth.validate_func'
```

## `urls.py`

```python
from django.urls import path

from django_light_auth import LoginView, LogoutView

urlpatterns = [
    # ...
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
]
```

## `your_app/auth/validate_func.py`
example at `django_light_auth.light_auth_validate_func`
```python
from typing import Dict, Any

from your_app.config import config

def light_auth_validate_func(data: Dict[str, Any]) -> bool:
    if data.get('username', None) == config.Auth.username and data.get(
        'password', None
    ) == config.Auth.password:
        return True

    return False
```

# Custom Login View 

`your_login_view.py`
```python
from django_light_auth import LoginView as LoginViewAbs


class LoginView(LoginViewAbs):
    template_name = 'your_app/login.html'
```
