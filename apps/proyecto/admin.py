from django.contrib import admin
from apps.proyecto.models import Proyecto, Tipo_metodologia, Rol

admin.site.register(Proyecto)
admin.site.register(Tipo_metodologia)
admin.site.register(Rol)

# Register your models here.
