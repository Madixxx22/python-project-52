from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.messages import error
from django.utils.translation import gettext as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin


class BaseRequiredMixin(LoginRequiredMixin, SuccessMessageMixin):
    success_url = ""
    error_url = ""
    login_url = reverse_lazy('login')
    success_message = _('The action is successful')
    permission_denied_message = _('The action went wrong')
    error_messages = _("You do not have permission")


class UserRequiredMixin(BaseRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if request.user.id == self.get_object().id:
            return super().dispatch(request, *args, **kwargs)
        error(request, self.error_messages)
        if request.user.is_authenticated:
            return redirect(self.success_url)
        else:
            return redirect(self.login_url)


class AuthorRequiredMixin(BaseRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if request.user.id == self.get_object().author.id:
            return super().dispatch(request, *args, **kwargs)
        error(request, self.error_messages)
        return redirect(self.error_url)
