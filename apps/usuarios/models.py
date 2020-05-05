from django.db import models
from django.contrib.auth.models import User


class Usuario(models.Model):
    celular = models.CharField(max_length=300, blank=True, null=True)
    id_user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
# Create your models here.

