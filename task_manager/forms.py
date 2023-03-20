from django.contrib.auth.forms import AuthenticationForm
from task_manager.users.models import CustomUser


class LoginForm(AuthenticationForm):

    class Meta():
        model = CustomUser
        fields = ('username', 'password')
