from django.urls import path
from task_manager.statuses.views import StatusesView, StatusCreateView,\
                                  StatusUpdateView, StatusDeleteView

app_name = 'statuses'

urlpatterns = [
    path('', StatusesView.as_view(), name="show_statuses"),
    path('create/', StatusCreateView.as_view(), name="create_status"),
    path('<int:pk>/update/', StatusUpdateView.as_view(), name="edit_status"),
    path('<int:pk>/delete/', StatusDeleteView.as_view(), name="delete_status"),
]
