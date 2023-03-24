from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from task_manager.mixins import BaseRequiredMixin

from task_manager.statuses.models import Statuses
from task_manager.statuses.forms import StatusForm


# Create your views here.
class StatusesView(BaseRequiredMixin, ListView):
    model = Statuses
    context_object_name = 'statuses'
    template_name = 'statuses/statuses.html'


class StatusCreateView(BaseRequiredMixin, CreateView):
    template_name = 'statuses/create_status.html'
    form_class = StatusForm
    success_url = reverse_lazy('statuses:show_statuses')
    success_message = _('Created status successfully')


class StatusUpdateView(BaseRequiredMixin, UpdateView):
    model = Statuses
    template_name = 'statuses/edit_status.html'
    form_class = StatusForm
    success_url = reverse_lazy('statuses:show_statuses')
    success_message = _('Updated status successfully')

    def get_queryset(self):
        return Statuses.objects.filter(id=self.kwargs['pk'])


class StatusDeleteView(BaseRequiredMixin, DeleteView):
    model = Statuses
    template_name = 'statuses/delete_status.html'
    success_url = reverse_lazy('statuses:show_statuses')
    success_message = _('Delete Status successfully')
    context_object_name = 'status'
