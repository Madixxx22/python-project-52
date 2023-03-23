from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.messages import error
from django.utils.translation import gettext as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, UpdateView, CreateView, \
                                 DeleteView, DetailView

from task_manager.tasks.models import Tasks
from task_manager.tasks.forms import TaskForm
from task_manager.users.models import CustomUser


# Create your views here.
class TasksView(LoginRequiredMixin, ListView):
    model = Tasks
    template_name = 'tasks/tasks.html'
    context_object_name = 'tasks'


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'tasks/create_task.html'
    form_class = TaskForm
    success_url = reverse_lazy('tasks:show_tasks')
    success_message = _('Created task successfully')

    def form_valid(self, form):
        user_pk = self.request.user.pk
        form.instance.author = CustomUser.objects.get(pk=user_pk)
        return super().form_valid(form)


class TaskDetailView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    model = Tasks
    template_name = 'tasks/detail_task.html'
    context_object_name = 'task'

    def get_queryset(self):
        return Tasks.objects.filter(id=self.kwargs['pk'])


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Tasks
    template_name = 'tasks/edit_task.html'
    form_class = TaskForm
    success_url = reverse_lazy('tasks:show_tasks')
    success_message = _('Updated task successfully')

    def get_queryset(self):
        return Tasks.objects.filter(id=self.kwargs['pk'])


class TaskDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Tasks
    template_name = 'tasks/delete_task.html'
    success_url = reverse_lazy('tasks:show_tasks')
    success_message = _('Delete task successfully')
    context_object_name = 'task'

    def dispatch(self, request, *args, **kwargs):
        if request.user.id == self.get_object().author.pk:
            return super().dispatch(request, *args, **kwargs)
        error(request, _("You do not have permission to delete the task"))
        return redirect(self.success_url)
