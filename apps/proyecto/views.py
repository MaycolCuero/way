from itertools import chain

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.core import serializers
from django.db.models import Count, Q
from datetime import date

from django.template.loader import render_to_string

from apps.proyecto.models import Proyecto, Rol, ProUser
from apps.proyecto.forms import ProyectoForm
from apps.scrum.models import Scrum, Pbacklog, HistoriaUsuario, Sbacklog, Sprint, DailyMeeting

from apps.usuarios.models import User, Usuario
from apps.xp.models import XP

import json


@login_required
def get_data(request, pro):
    return redirect('/proyecto/index/'+str(pro))


@login_required
def index(request, id):
    p = Proyecto.objects.filter(id=id)
    sprint = Sprint.objects.filter(estado=True, id_scrum__proyecto__id=p[0].id)
    sprint_to_confirm = Sprint.objects.filter(estado=False, confirmar=True, id_scrum__proyecto__id=p[0].id)
    if sprint_to_confirm:
        id_sprint_cf = sprint_to_confirm[0].id
        alcanzados = Pbacklog.objects.filter(estado=True, id_scrum__proyecto__id=id, sprint__id=id_sprint_cf)
    else:
        alcanzados = ""

    if sprint:
        id_sprint = sprint[0].id
        
        backlog = Pbacklog.objects.filter(sprint__id=id_sprint, estado=False).annotate(
            historias=Count('historiausuario__id')
        )

        historic = HistoriaUsuario.objects.filter(id_pbacklog__sprint__id=id_sprint)
        tareas = Sbacklog.objects.filter(id_historia__id_pbacklog__sprint__id=id_sprint, get=False)
        hechas = Sbacklog.objects.filter(id_historia__id_pbacklog__sprint__id=id_sprint, estado=True)
        haciendo = Sbacklog.objects.values('id','nombre', 'usuario__first_name','usuario__last_name','usuario__id').filter(
            id_historia__id_pbacklog__sprint__id=id_sprint,
            get=True,
            estado=False
        )
        info = Sprint.objects.get(estado=True, id_scrum__proyecto__id=p[0].id)
        var = info.f_fin - date.today()
    else:
        backlog = ""
        historic = ""
        tareas = ""
        hechas = ""
        haciendo = ""
        info = ""
        var = ""
        sprint = Sprint.objects.filter(estado=False, confirmar=True, id_scrum__proyecto__id=p[0].id)
        if sprint:
            id_sprint = sprint[0].id
        else:
            id_sprint =""


    integrantes = ProUser.objects.values(
        'usuario__username',
        'usuario__first_name',
        'usuario__last_name',
        'rol__nombre',
        'horas'
    ).filter(proyecto=id)
    
    rol = ProUser.objects.values('rol__nombre').filter(proyecto=id,usuario=request.user.pk)
    print('rol del actualmente conectado',rol)

    #listado de requisitos terminados y sin terminar
    f = Pbacklog.objects.filter(estado=False, id_scrum=22)

    r = Pbacklog.objects.filter(estado=True, id_scrum=22)

    #la siguiente consulta obtendra la lista de cada daylimeeting registrado hasta el momento en que se realiza la consulta.
    meetingsday = DailyMeeting.objects.values('usuario__first_name','usuario__last_name','ayer','hoy','problemas').filter(
        sprint__estado=True, sprint__id_scrum__proyecto__id=id
    )

    resumen = resumenScrum(id)
    resumen_requisitos = resumen['requisitos']
    resumen_proyecto = resumen['proyecto']
    resumen_integrantes = resumen['integrantes']
    resumen_sprints = resumen['sprint']
    datos1 = resumen_sprints['datos1']
    datos2 = resumen_sprints['datos2']
    resumen_tareas = resumen['tareas']
    resumen_daily = resumen['daily']

    contexto = {'pbacklog': backlog,
                'historia': historic,
                'tareas': tareas,
                'proyecto': p,
                'idIndex': id,
                'haciendo': haciendo,
                'hechas': hechas,
                'integrantes': integrantes,
                'sprint': id_sprint,
                'info': info,
                'var': var,
                'Rterminados':r,
                'RsinTerminar':f,
                'alcanzados': alcanzados,
                'meetingsday': meetingsday,
                'rol':rol,
                'resumen_proyecto':resumen_proyecto,
                'resumen_requisitos':resumen_requisitos,
                'resumen_integrantes':resumen_integrantes,
                'resumen_sprints_datos1':datos1,
                'resumen_sprints_datos2':datos2,
                'resumen_tareas':resumen_tareas,
                'resumen_daily':resumen_daily
    }

    return render(request, 'proyecto/index.html', contexto)


@login_required
def requisitos():
    t = Pbacklog.objects.filter(estado=False, id_scrum=22)
    r = Pbacklog.objects.filter(estado=True, id_scrum=22)
    s = t | r
    pass


@login_required
def index2(request):
    id = request.session['proyectoIndex']
    return index(request,id)


@login_required
def proyecto_crear(request):
    usuario = request.user.pk
    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        # form.fields['usuario'] = request.session['id_user']#porque no da.
        if form.is_valid():
            # guardo el proyecto
            m = form.save()
            # get id user from POST method
            u = User.objects.get(id=usuario)
            midle = ProUser(usuario=u, proyecto=m, horas=40)
            midle.save()
            # realizo una consulta para saber la metodologia elegida
            print(form)
            if request.POST["id_metodologia"] == "1":  # pregunta si la metodologia es scrum
                b = Scrum.objects.create(proyecto=m)  # crear el registro en scrum con el id del proyecto.
                rol = Rol.objects.get(nombre="Product Owner")
                ProUser.objects.filter(id=midle.id).update(rol=rol.id)
                request.session['scrum'] = b.id
                return redirect('scrum:pbacklog_crear')
            elif request.POST['id_metodologia'] == '2':
                x = XP.objects.create(proyecto=m)
                rol = Rol.objects.get(nombre='Manager')
                ProUser.objects.filter(id=midle.id).update(rol=rol.id)
                request.session['xp']=x.id
                return redirect('xp:CrearHistorias')
            else:
                return redirect('usuarios:index')
    else:
        form = ProyectoForm()
    return render(request, 'proyecto/proyecto_form.html', {'form': form, 'usuario': usuario})


@login_required
def proyecto_list(request):
    proyecto = Proyecto.objects.all().order_by('id')
    contexto = {'proyecto': proyecto}
    return render(request, 'proyecto/proyecto_list.html', contexto)


@login_required
def estado(request):
    if request.method == 'POST':
        print('datos del formulario',request.POST)
        id = request.POST['id']

        #idIndex = request.POST['idIndex']  # el idIndex es el id que le pertenece al proyecto
        id_sprint = request.POST['sprint']

        idUser = request.user.pk
        Sbacklog.objects.filter(id=id).update(usuario=idUser, get=True)
        # Sbacklog.objects.filter(id=id).update(get=True)
        tareas = Sbacklog.objects.filter(id_historia__id_pbacklog__sprint__id=id_sprint, get=False)
        hechas = Sbacklog.objects.filter(id_historia__id_pbacklog__sprint__id=id_sprint, estado=True)
        haciendo = Sbacklog.objects.values('id','nombre', 'usuario__first_name','usuario__last_name','usuario__id').filter(
            id_historia__id_pbacklog__sprint__id=id_sprint,
            get=True,
            estado=False
        )
        contexto = {
            'pendientes': tareas,
            'hechas':hechas,
             'haciendo':haciendo,
            'user_pk':idUser,
            'sprint':id_sprint,
            'idIndex':request.POST['idIndex']
        }

    datos = {'listTareas': render_to_string('clean/tablero_scrum.html',contexto)}

    return JsonResponse(datos)


@login_required
def tareas(request):
    usuario = request.session['id_user']
    if request.method == 'POST':
        idUser = request.session['id_user']
        id = request.POST['id']
        idIndex = request.POST['idIndex']  # el idIndex es el id que le pertenece al proyecto
        Sbacklog.objects.filter(id=id).update(usuario=idUser)
        return index(request, idIndex)
    return render(request, 'usuarios/tareas.html', {'usuario': usuario})


@login_required
def integrante(request):
    print('datos enviados del integrante', request.POST)
    if request.method == "POST":

        email = request.POST['email']
        try:
            usuario = User.objects.get(email=email)
        except:
            usuario = ""
        pro = request.POST['idIndex']

        if usuario != "":
            validar = ProUser.objects.filter(usuario=usuario.id, proyecto=pro)
            if validar:
                pass
            else:
                r = request.POST['rol']
                rol = Rol.objects.get(nombre=r)
                horas = request.POST['horas']

                proyecto = Proyecto.objects.get(id=pro)
                guardar = ProUser(usuario=usuario, proyecto=proyecto, disponible=True, rol=rol, horas=horas)
                guardar.save()
    return JsonResponse({'datos':'ready'})


@login_required
def actualizarHistorias(request):
    if request.method == 'GET':
        id = request.GET['id']
        d = HistoriaUsuario.objects.filter(id_pbacklog=id).annotate(
            tareas=Count('sbacklog__id'),
            hechas=Count('sbacklog__id', filter=Q(sbacklog__estado=True))
        )
        datos = serializers.serialize('json', d)

    return HttpResponse(datos, content_type='application/json')


@login_required
def getTareas(request):
    if request.method == 'GET':
        id = request.GET['id']
        d = Sbacklog.objects.filter(id_historia=id, get=False)
        datos = serializers.serialize('json', d, fields=('id', 'nombre'))
    else:
        print("hubo algun error")

    return HttpResponse(datos, content_type='application/json')


@login_required
def getTareasDetalle(request):
    if request.method == 'GET':
        id = request.GET['id']
        d = Sbacklog.objects.filter(id=id)
        datos = serializers.serialize('json', d)
    else:
        print("hubo algun error")

    return HttpResponse(datos, content_type='application/json')


@login_required
def actualizarTarea(request):
    if request.method == 'POST':
        id = request.POST['id']
        nombre = request.POST['nombre']
        n_horas = request.POST['n_horas']
        s = Sbacklog.objects.filter(id=id).update(nombre=nombre, n_horas=n_horas)

    return HttpResponse('success')
# Create your views here.


def resumenScrum(id_proyecto):
    p = Proyecto.objects.values('nombre','f_inicio','f_fin').filter(id=id_proyecto)
    requisitos = HistoriaUsuario.objects.values(
        'id_pbacklog__nombre','como_usuario','quiero','para'
    ).filter(id_pbacklog__id_scrum__proyecto=id_proyecto)

    integrantes = ProUser.objects.values(
        'usuario__first_name',
        'usuario__last_name',
        'rol__nombre'
    ).filter(proyecto=id_proyecto)

    sprint1 = Sprint.objects.values('id','f_inicio','f_fin').filter(id_scrum__proyecto=id_proyecto).distinct()
    sprint = Sprint.objects.values(
        'id',
        'f_inicio',
        'f_fin',
        'id_pbacklog__historiausuario__como_usuario',
        'id_pbacklog__historiausuario__quiero',
        'id_pbacklog__historiausuario__para'
    ).filter(id_scrum__proyecto=id_proyecto)

    #creo una matriz para poder comparar  las fechas y asi mostrar la misma informacion
    matriz = {'datos1':sprint1,
    'datos2':sprint}

    tareas = Sbacklog.objects.values(
        'nombre',
        'n_horas',
        'usuario__first_name',
        'usuario__last_name',
        'id_historia__id_pbacklog__sprint__id'
    ).filter(estado=True,id_historia__id_pbacklog__id_scrum__proyecto=id_proyecto)

    daily = DailyMeeting.objects.values(
        'usuario__first_name',
        'usuario__last_name',
        'ayer',
        'hoy',
        'problemas',
        'sprint',
        'hora'
    ).filter(sprint__id_scrum__proyecto=id_proyecto)

    contexto = {
        'proyecto':p,
        'requisitos':requisitos,
        'integrantes': integrantes,
        'sprint':matriz,
        'tareas': tareas,
        'daily':daily
    }

    return contexto