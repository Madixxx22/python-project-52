from django.urls import path
from task_manager.users import views

app_name = 'users'

urlpatterns = [
    path('', views.UserView.as_view(), name='show_users'),
    path('create/', views.UserCreateView.as_view(), name='register'),
    path('<int:pk>/update/', views.UserUpdateView.as_view(), name='edit_user'),
    path('<int:pk>/delete/', views.UserDeleteView.as_view(), name='delete_user'),
]
