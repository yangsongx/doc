from django.db import models

# Create your models here.
class Account(models.Model):
    user_name = models.CharField(max_length=30)
    user_type = models.BigIntegerField(blank=True,null=True)
    password = models.CharField(max_length=128)
    active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

