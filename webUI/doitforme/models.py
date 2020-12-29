from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Servers(models.Model):
    ip_address = models.GenericIPAddressField()
    password = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'servers'
