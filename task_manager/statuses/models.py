from django.db import models


# Create your models here.
class Statuses(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_date = models.DateField(auto_now_add=True)
