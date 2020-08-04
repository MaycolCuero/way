from django.conf.urls import url
from django.urls import path
from apps.scrum.views import scrum_list, scrum_crear, pbacklog_crear, pbacklog_list, historia_crear, update_pbacklog, eliminarPbacklog
from apps.scrum.views import sbacklog_estado, historia_list, sbacklog_crear, sbacklog_list, sprint, dailymeeting, sreview
from apps.scrum import views
app_name = 'scrum'

urlpatterns = [

    url(r'^scrum_crear$', scrum_crear, name='scrum_crear'),
    url(r'^scrum_list$', scrum_list, name='scrum_list'),
    url(r'^pbacklog_crear$', pbacklog_crear, name='pbacklog_crear'),
    url(r'^pbacklog_list$', pbacklog_list, name='pbacklog_list'),
    url(r'^historia_crear$', historia_crear, name='historia_crear'),
    url(r'^historia_list$', historia_list, name='historia_list'),
    url(r'^sbacklog_crear$', sbacklog_crear, name='sbacklog_crear'),
    url(r'^sbacklog_list$', sbacklog_list, name='sbacklog_list'),
    url(r'^sbacklog_estado$', sbacklog_estado, name='sbacklog_estado'),
    url(r'^sprint/(?P<id>\d+)/$', sprint, name='sprint'),
    path('dailymeeting', dailymeeting, name='dailymeeting'),
    path('sreview', sreview, name='sreview'),
    path('update_pbacklog', update_pbacklog, name='update_pbacklog'),
    path('eliminarPbacklog', eliminarPbacklog, name='eliminarPbacklog'),
    path('update_epica', views.update_epica, name='update_epica'),
    path('delete_epica', views.delete_epica, name='delete_epica'),
    path('update_historia', views.update_historia, name='update_historia'),
    path('delete_historia', views.delete_historia, name='delete_historia'),
    path('delete_tarea', views.delete_tarea, name='delete_tarea'),
    path('edit_epicas_sprint', views.edit_epica_sprint, name="edit_epicas_sprint"),
    path('listado_historias_sprint', views.listado_historias_sprint, name="listado_historias_sprint"),
    path('editar_historias_sprint', views.editar_historia_sprint, name="editar_historias_sprint"),
    path('eliminar_historia', views.eliminar_historia, name="eliminar_historia"),
    path('tabla_tareas_sprint', views.tabla_tareas_sprint, name="tabla_tareas_sprint"),
    path('add_tarea_sprint', views.add_tarea_sprint, name="add_tarea_sprint"),
    path('update_tarea_sprint', views.update_tarea_sprint, name="update_tarea_sprint"),
    path('delete_tarea_sprint', views.delete_tarea_sprint, name="delete_tarea_sprint"),

]
