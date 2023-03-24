from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import ListView, UpdateView, CreateView, \
                                 DeleteView, DetailView
from task_manager.mixins import AuthorRequiredMixin, BaseRequiredMixin

from task_manager.tasks.models import Tasks
from task_manager.tasks.forms import TaskForm
from task_manager.users.models import CustomUser


# Create your views here.
class TaskBase():

    def get_queryset(self):
        return Tasks.objects.filter(id=self.kwargs['pk'])


class TasksView(BaseRequiredMixin, ListView):
    model = Tasks
    template_name = 'tasks/tasks.html'
    context_object_name = 'tasks'


class TaskCreateView(BaseRequiredMixin, CreateView):
    template_name = 'tasks/create_task.html'
    form_class = TaskForm
    success_url = reverse_lazy('tasks:show_tasks')
    success_message = _('Created task successfully')

    def form_valid(self, form):
        user_pk = self.request.user.pk
        form.instance.author = CustomUser.objects.get(pk=user_pk)
        return super().form_valid(form)


class TaskDetailView(BaseRequiredMixin, TaskBase, DetailView):
    model = Tasks
    template_name = 'tasks/detail_task.html'
    context_object_name = 'task'


class TaskUpdateView(BaseRequiredMixin, TaskBase, UpdateView):
    model = Tasks
    template_name = 'tasks/edit_task.html'
    form_class = TaskForm
    success_url = reverse_lazy('tasks:show_tasks')
    success_message = _('Updated task successfully')


class TaskDeleteView(AuthorRequiredMixin, DeleteView):
    model = Tasks
    template_name = 'tasks/delete_task.html'
    success_url = reverse_lazy('tasks:show_tasks')
    error_url = reverse_lazy('tasks:show_tasks')
    success_message = _('Delete task successfully')
    context_object_name = 'task'
    error_messages = _("You do not have permission to delete the task")
