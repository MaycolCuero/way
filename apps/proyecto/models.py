from django.db import models
from django.contrib.auth.models import User
from apps.usuarios.models import Usuario
from django.utils import timezone


class Tipo_metodologia(models.Model):
    nombre = models.CharField(max_length=500)

    def __str__(self):
        return '{}'.format(self.nombre)


class Proyecto(models.Model):
    nombre = models.CharField(max_length = 500)
    fecha = models.DateTimeField(default=timezone.now)
    f_inicio = models.DateField(null = True, blank = True)
    f_fin = models.DateField(null = True, blank = True)
    id_metodologia = models.ForeignKey(Tipo_metodologia, null =True, blank = True, on_delete = models.CASCADE)
    usuario = models.ManyToManyField(User, through='ProUser')

    def __str__(self):
        return '{}'.format(self.nombre)
# Create your models here.


class Rol(models.Model):
    metodologia = models.ForeignKey(Tipo_metodologia, null=True, blank=True, on_delete=models.CASCADE)
    nombre = models.CharField(max_length= 300,null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.nombre)


class ProUser(models.Model):
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    proyecto = models.ForeignKey(Proyecto, null=True, blank=True, on_delete=models.CASCADE)
    disponible = models.BooleanField(null=True, blank=True)
    horas = models.IntegerField(null=True, blank=True)
    rol = models.ForeignKey(Rol, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.proyecto)


# Create your models here.
