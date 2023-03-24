from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from task_manager.mixins import UserRequiredMixin
from task_manager.users.forms import CustomUserCreationForm, \
                                     CustomUserChangeForm
from task_manager.users.models import CustomUser


# Create your views here.
class UserView(ListView):
    model = CustomUser
    context_object_name = 'users'
    template_name = 'users/users.html'


class UserCreateView(SuccessMessageMixin, CreateView):
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    success_message = _("User is successfully registered")


class UserUpdateView(UserRequiredMixin, UpdateView):
    model = CustomUser
    template_name = 'users/edit_user.html'
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('users:show_users')
    success_message = _("User is changed successfully")
    permission_denied_message = _('You are not logged in, log in!')

    def get_queryset(self):
        return CustomUser.objects.filter(id=self.kwargs['pk'])


class UserDeleteView(UserRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'users/delete_user.html'
    success_url = reverse_lazy('users:show_users')
    context_object_name = 'user'
    success_message = _("User is deleted successfully")
