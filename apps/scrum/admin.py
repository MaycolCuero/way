from django.contrib import admin
from apps.scrum.models import Scrum, Pbacklog, HistoriaUsuario, Sbacklog, Sreview

admin.site.register(Scrum)
admin.site.register(Pbacklog)
admin.site.register(HistoriaUsuario)
admin.site.register(Sbacklog)
admin.site.register(Sreview)
# Register your models here.
