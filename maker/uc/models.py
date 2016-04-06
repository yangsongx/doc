from __future__ import unicode_literals
from django.db import models

# Create your models here.
class Account(models.Model):
    user_name = models.CharField(max_length=30)
    user_type = models.BigIntegerField(blank=True,null=True)
    password = models.CharField(max_length=123)
    created = models.DateTimeField(auto_now_add=True)
