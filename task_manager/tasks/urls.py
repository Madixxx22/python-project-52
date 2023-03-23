from django.urls import path

from task_manager.tasks.views import TasksView, TaskCreateView,\
                                     TaskDetailView, TaskUpdateView, \
                                     TaskDeleteView

app_name = 'tasks'

urlpatterns = [
    path('', TasksView.as_view(), name='show_tasks'),
    path('create/', TaskCreateView.as_view(), name='create_task'),
    path('<int:pk>/', TaskDetailView.as_view(), name='detail_task'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='edit_task'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='delete_task'),
]
