from django.conf.urls import url
from django.urls import path

from apps.proyecto.views import proyecto_crear, proyecto_list, index, estado, integrante, actualizarHistorias, index2, getTareas, getTareasDetalle, actualizarTarea
app_name = 'proyecto'

urlpatterns = [
   # path('index/', index, name='index' ),
    url(r'^nuevo$', proyecto_crear, name='crear_proyecto'), 
    url(r'^listar$', proyecto_list, name='listar_proyecto'),
    url(r'^index/(?P<id>\d+)/$', index, name='index'),
    url(r'^estado$', estado, name='estado'),
    url(r'^actualizarHistorias$', actualizarHistorias, name='actualizarHistorias'),
    url(r'^integrante$', integrante, name='integrante'),
    path('index2', index2, name='index2'),
    path('getTareas', getTareas, name='getTareas'),
    path('getTareasDetalle', getTareasDetalle, name='getTareasDetalle'),
    path('actualizarTarea', actualizarTarea, name='actualizarTarea'),
]
