from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.messages import info
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView

from task_manager.forms import LoginForm


class IndexView(TemplateView):
    template_name = 'index.html'


class LoginView(SuccessMessageMixin, LoginView):
    template_name = 'login.html'
    form_class = LoginForm
    next_page = reverse_lazy('homepage')
    success_message = 'Login successful'


class LogoutView(LogoutView):
    next_page = reverse_lazy('homepage')
    success_message = 'You logged out of your account'

    def dispatch(self, request, *args, **kwargs):
        info(request, self.success_message)
        return super().dispatch(request, *args, **kwargs)
