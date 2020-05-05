from django.db import models
from apps.proyecto.models import Proyecto

# Create your models here.


class XP(models.Model):
    proyecto = models.ForeignKey(Proyecto, null=True, blank=True, on_delete=models.CASCADE)


class Ciclo(models.Model):
    f_inicio = models.DateTimeField()
    f_fin = models.DateTimeField()
    id_xp = models.ForeignKey(XP, null=True, blank=True, on_delete=models.CASCADE)
    estado = models.BooleanField(null=True, blank=True)