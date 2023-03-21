from django import forms
from django.utils.translation import gettext as _
from task_manager.users.models import CustomUser
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    password = forms.CharField(label=_("Password"))
    class Meta():
        model = CustomUser
        fields = ('username', 'password')
