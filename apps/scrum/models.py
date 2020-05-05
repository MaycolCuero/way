from django.utils import timezone
from django.db import models
from apps.usuarios.models import Usuario, User
from apps.proyecto.models import Proyecto
from apps.xp.models import XP, Ciclo

# Create your models here.


class Scrum(models.Model):
    proyecto = models.ForeignKey(Proyecto, null=True, blank=True, on_delete=models.CASCADE)


class Pbacklog(models.Model):
    nombre = models.CharField(max_length = 300)
    quiero = models.CharField(max_length=300, null=True, blank=True)
    para = models.CharField(max_length=300, null=True, blank=True)
    id_scrum = models.ForeignKey(Scrum, null = True, blank = True, on_delete = models.CASCADE)
    estado = models.BooleanField(null=True, blank=True)
    confirmar = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.nombre)


class HistoriaUsuario(models.Model):
    como_usuario = models.CharField(max_length = 300)
    quiero = models.TextField()
    para = models.TextField()
    estado = models.BooleanField(null=True, blank=True)
    get = models.BooleanField(null=True, blank=True) #nos servira para identificar si la tarea fue obtenida para realizarse en un ciclo en alguna metodologia
    id_pbacklog = models.ForeignKey(Pbacklog, null = True, blank = True, on_delete = models.CASCADE)
    id_xp = models.ForeignKey(XP, null = True, blank = True, on_delete = models.CASCADE)
    id_ciclo = models.ForeignKey(Ciclo, null = True, blank = True, on_delete = models.CASCADE)
    usuario = models.ManyToManyField(User)

    def __str__(self):
        return '{}'.format(self.quiero)


class Sbacklog(models.Model):
    nombre = models.TextField()
    n_horas = models.IntegerField()
    estado = models.BooleanField(null=True, blank=True)
    get = models.BooleanField(null=True, blank=True)
    usuario = models.ForeignKey(User, null = True, blank= True, on_delete = models.CASCADE)
    id_historia = models.ForeignKey(HistoriaUsuario, null = True, blank =True, on_delete = models.CASCADE)

    def __str__(self):
        return '{}'.format(self.nombre)


class Sprint(models.Model):
    f_inicio = models.DateField(blank=True, null=True)
    f_fin = models.DateField(blank=True, null=True)
    id_scrum = models.ForeignKey(Scrum, null=True, blank=True, on_delete=models.CASCADE)
    id_pbacklog = models.ManyToManyField(Pbacklog)
    estado = models.BooleanField(null=True, blank=True)
    confirmar = models.BooleanField(null=True, blank=True)



class Sreview(models.Model):
    logros = models.CharField(max_length=600, blank=True, null=True)
    observaciones = models.CharField(max_length=600,  blank=True, null=True)
    sprint = models.ForeignKey(Sprint, blank=True, null=True, on_delete=models.CASCADE)
    id_pbacklog = models.ManyToManyField(Pbacklog, blank=True, null=True)


class DailyMeeting(models.Model):
    ayer = models.CharField(max_length=300)
    hoy = models.CharField(max_length=300)
    problemas = models.CharField(max_length=300)
    usuario = models.ForeignKey(User,on_delete=models.CASCADE)
    sprint = models.ForeignKey(Sprint,blank=True, null=True, on_delete=models.CASCADE)
    hora = models.DateTimeField(default=timezone.now)
# Create your models here.
