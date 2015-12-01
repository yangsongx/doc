from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Account(models.Model):
    usr = models.ForeignKey(User, unique=True, verbose_name='MyUser')
    user_type = models.BigIntegerField(blank=True, null=True)


