from django import http
from django.urls import reverse_lazy
from django.contrib.messages import info
from django.views.generic import TemplateView
from django.utils.translation import gettext as _
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin

from task_manager.forms import LoginForm


class IndexView(TemplateView):
    template_name = 'index.html'


class LoginView(SuccessMessageMixin, LoginView):
    template_name = 'form.html'
    form_class = LoginForm
    next_page = reverse_lazy('homepage')
    success_message = _('Login successful')
    extra_context = {
        'title': _('Login'),
        'button': _('Login')
    }


class LogoutView(LogoutView):
    next_page = reverse_lazy('homepage')
    success_message = _('You logged out of your account')

    def dispatch(
        self,
        request: http.HttpRequest,
        *args: tuple,
        **kwargs: dict
    ) -> http.HttpResponse:
        info(request, self.success_message)
        return super().dispatch(request, *args, **kwargs)
