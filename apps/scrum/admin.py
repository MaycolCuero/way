from django.contrib import admin
from apps.scrum.models import Scrum, Pbacklog, HistoriaUsuario, Sbacklog, Sreview, DailyMeeting

admin.site.register(Scrum)
admin.site.register(Pbacklog)
admin.site.register(HistoriaUsuario)
admin.site.register(Sbacklog)
admin.site.register(Sreview)
admin.site.register(DailyMeeting)
# Register your models here.
