from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.messages import error
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from task_manager.users.forms import CustomUserCreationForm, CustomUserChangeForm
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
    success_message = "User is successfully registered"


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = CustomUser
    template_name = 'users/edit_user.html'
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('users:show_users')
    success_message = "User is changed successfully"
    login_url = reverse_lazy('login')
    permission_denied_message = 'You are not logged in, log in!'

    def get_queryset(self):
        return CustomUser.objects.filter(id=self.kwargs['pk'])

    def dispatch(self, request, *args, **kwargs):
        if request.user.id == self.get_object().id:
            return super().dispatch(request, *args, **kwargs)
        error(request, "You do not have permission to change the user")
        return redirect(self.success_url)


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'users/delete_user.html'
    success_url = reverse_lazy('users:show_users')
    context_object_name = 'user'

    def dispatch(self, request, *args, **kwargs):
        if request.user.id == self.get_object().id:
            return super().dispatch(request, *args, **kwargs)
        error(request, "You do not have permission to delete the user")
        return redirect(self.success_url)
