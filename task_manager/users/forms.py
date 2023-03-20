from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from task_manager.users.models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("username", "first_name", "last_name")


class CustomUserChangeForm(UserChangeForm):
    password = forms.CharField(
        label='New password',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        required=False,
    )

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
