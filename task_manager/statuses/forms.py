from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext as _

from task_manager.statuses.models import Statuses

class StatusForm(ModelForm):
    name = forms.CharField(label=_("Name"))
    class Meta():
        model = Statuses
        fields = ['name']