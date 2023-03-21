from django import forms
from django.utils.translation import gettext as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from task_manager.users.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label=_("First Name"))
    last_name = forms.CharField(label=_("Last Name"))
    class Meta:
        model = CustomUser
        fields = ("username", "first_name", "last_name")


class CustomUserChangeForm(UserChangeForm):
    password = forms.CharField(
        label=_('New password'),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        required=False,
    )
    first_name = forms.CharField(label=_("First Name"))
    last_name = forms.CharField(label=_("Last Name"))

    class Meta:
        model = CustomUser
        fields = ("username", "first_name", "last_name", "password")

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')

        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user
