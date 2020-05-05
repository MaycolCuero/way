from django.conf.urls import url
from django.urls import path
from apps.usuarios.views import register,  index, logout, perfil, tareas, confirmar, getTareas, getTareasHechas, Login

app_name = 'usuarios'

urlpatterns = [
    #path('index', index, name='index'),
    url(r'^register$', register, name='register'),
    #url(r'^login$', login, name='login'),
    url(r'^index$', index, name='index'),

    url(r'^logout$', logout, name='logout'),
    url(r'^perfil$', perfil, name='perfil'),
    url(r'^tareas$', tareas, name='tareas'),
    url(r'^confirmar$', confirmar, name='confirmar'),
    path('getTareas', getTareas, name='getTareas'),
    path('getTareasHechas', getTareasHechas, name='getTareasHechas'),
    path('login', Login.as_view(), name='login'),

]
