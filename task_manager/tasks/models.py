from django.db import models
from task_manager.statuses.models import Statuses

from task_manager.users.models import CustomUser


# Create your models here.
class Tasks(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=1048576)
    created_date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.RESTRICT,
        related_name='author'
    )
    status = models.ForeignKey(
        Statuses,
        on_delete=models.RESTRICT,
        related_name='status'
    )
    executor = models.ForeignKey(
        CustomUser,
        on_delete=models.RESTRICT,
        related_name='executor'
    )
