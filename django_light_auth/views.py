from django import forms
from django.views.generic import View, FormView
from django.http import HttpResponseRedirect
from django.contrib import messages

from .runtimes import do_login, do_logout, do_validate


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    # next = forms.CharField()


class LoginView(FormView):
    template_name = 'django_light_auth/login.html'
    form_class = LoginForm
    initial = dict()

    def get(self, request, *args, **kwargs):
        # next
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        if do_validate(form.cleaned_data):
            self.success_url = do_login(self.request)
            return HttpResponseRedirect(self.success_url)

        messages.add_message(
            self.request, messages.ERROR,
            'Invalid username and/or password! Please try again.'
        )
        self.initial['username'] = form.cleaned_data['username']
        return HttpResponseRedirect(self.request.path)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(do_logout(request))
