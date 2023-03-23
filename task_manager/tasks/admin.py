from django.contrib import admin

from task_manager.tasks.models import Tasks

# Register your models here.
admin.site.register(Tasks)
