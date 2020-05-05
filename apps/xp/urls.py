from django.conf.urls import url
from django.urls import path
from apps.xp.views import CrearHistorias, CrearTareas, ActualizarHistorias, eliminarHistoria, index, crearCiclo, agregar_integrantes, obtener

app_name = 'xp'

urlpatterns = [
    path('CrearHistorias/', CrearHistorias.as_view(), name='CrearHistorias'),
    path('CrearTareas/', CrearTareas.as_view(), name='CrearTareas'),
    path('ActualizarHistorias/<int:pk>', ActualizarHistorias.as_view(), name='ActualizarHistorias'),
    path('eliminar_historias/<int:id>', eliminarHistoria, name='eliminar_historias'),
    path('index-xp/<int:id>', index, name='index-xp'),
    path('crearCiclo', crearCiclo, name='crearCiclo'),
    path('agregar_integrantes', agregar_integrantes, name="agregar_integrantes"),
    path('obtener', obtener, name='obtener'),
]
