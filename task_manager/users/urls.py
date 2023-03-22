from django.urls import path
from task_manager.users.views import UserView, UserCreateView,\
                               UserUpdateView, UserDeleteView

app_name = 'users'

urlpatterns = [
    path('', UserView.as_view(), name='show_users'),
    path('create/', UserCreateView.as_view(), name='register'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='edit_user'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='delete_user'),
]
