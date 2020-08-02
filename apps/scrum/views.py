from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.core import serializers

from apps.scrum.models import Pbacklog, Sbacklog, HistoriaUsuario, Sprint, Scrum, DailyMeeting, Sreview
from apps.scrum.forms import ScrumForm, PbacklogForm, HistoriaUsuarioForm, SbacklogForm, SprintForm, SreviewFrom
from apps.proyecto.views import get_data
from apps.usuarios.models import User
from apps.proyecto.models import Proyecto, ProUser
from django.db.models import Count, Q, Sum


@login_required
def scrum_list(request):
    backlog = Pbacklog.objects.all()
    contexto = {'pbacklog':backlog}
    return render(request, 'scrum/pbacklog_list',contexto)


@login_required
def pbacklog_list(request):
    backlog = Pbacklog.objects.all()
    contexto = {'pbacklog':backlog}
    return render(request, 'scrum/pbacklog_list.html',contexto)


@login_required
def historia_list(request):
    scrum = request.session['scrum']
    id_proyecto = Proyecto.objects.get(scrum__id=scrum)

    historia = HistoriaUsuario.objects.filter(id_pbacklog__id_scrum=scrum).annotate(
        tarea = Count('sbacklog__id')
    ).order_by('id')
    tareas = Sbacklog.objects.values('id','nombre','id_historia__quiero','n_horas').filter(id_historia__id_pbacklog__id_scrum=scrum)
    contexto = {
        'historia':historia,
        'tareas':tareas,
        'id_proyecto':id_proyecto
    }
    return render(request, 'scrum/historia_list.html', contexto)


@login_required
def sbacklog_list(request):
    scrum = request.session['scrum']
    sbacklog = Sbacklog.objects.filter(id_historia__id_pbacklog__id_scrum=scrum).order_by('id')
    contexto = {'sbacklog':sbacklog}
    return render(request, 'scrum/sbacklog_list.html', contexto)


@login_required
def scrum_crear(request):
    form = ScrumForm
    if request.method == 'POST':
        form = ScrumForm(data=request.POST)
        if form.is_valid():
           scrum =  form.save()
           # guardo el id del proyecto scrum
           request.session['scrum'] = scrum.id
           #return redirect('scrum:scrum_list')
           return redirect('scrum:pbacklog_crear')


    return render(request, 'scrum/scrum_crear.html',{'form':form})


@login_required
def pbacklog_crear(request):
    # creo un objeto con el ide del proyecto de scrum
    scrum = request.session['scrum']
    backlog = Pbacklog.objects.filter(id_scrum=scrum).annotate(
        hu=Count('historiausuario__id')
    ).order_by('id')

    if request.method == 'POST':
        form = PbacklogForm(data=request.POST)
        #print(form)
        if form.is_valid():
            form.save()
            print('paso')
            datos = {'datos': render_to_string('clean/scrum/table_epicas.html', {'pbacklog': backlog, 'scrum': scrum})}
            #return redirect('scrum:pbacklog_crear')
            return JsonResponse(datos)
        else:
            print('no se guardo')
    else:
        form = PbacklogForm

    return render(request, 'scrum/pbacklog_crear.html',{'form':form, 'scrum':scrum, 'pbacklog':backlog})


@login_required
def historia_crear(request):
    try:
        scrum = request.POST['scrum']
    except:
        scrum = ""

    if scrum:
        backlog = Pbacklog.objects.filter(id_scrum=scrum).annotate(
            hu=Count('historiausuario__id')
        ).order_by('id')
    try:
        sprint = request.POST['sprint']
    except:
        sprint = ""

    print('datos enviados para crear historias', request.POST)
    if request.method == 'POST':
        form = HistoriaUsuarioForm(data=request.POST)
        if form.is_valid():
            form.save()
            if sprint:
                id_pbacklog = request.POST['id_pbacklog']
                data = datos_sprint(id_pbacklog)

                datos = {
                    'tabla_general': render_to_string('clean/scrum/tabla_epicas_general_sprint.html',
                                                      {'requisitos': data['requisitos']}),
                    'tabla_editar_epica': render_to_string('clean/scrum/tabla_editar_epicas_sprint.html',
                                                           {'requisitos': data['requisitos']}),
                    'modulo_historia': render_to_string('clean/scrum/edicion_historias.html', {'historias': data['historias'],
                        'id_pbacklog': id_pbacklog}
                        )
                    }
                #datos = {'datos':'recibidos'}
            else:
                datos = {'datos': render_to_string('clean/scrum/table_epicas.html', {'pbacklog': backlog, 'scrum': scrum})}
            return JsonResponse(datos)
    else:
        form = HistoriaUsuarioForm
    #return render(request, 'scrum/pbacklog_crear.html', {'formHistoria': form})
    return pbacklog_crear(request)


@login_required
def sbacklog_crear(request):
    if request.method == 'POST':
        form = SbacklogForm(data=request.POST)
        if form.is_valid():
            form.save()

    id_pro = request.POST['id_pro']
    scrum = request.session['scrum']

    historia = HistoriaUsuario.objects.filter(id_pbacklog__id_scrum=scrum).annotate(
                tarea=Count('sbacklog__id')
            ).order_by('id')

    tareas = Sbacklog.objects.values('id','nombre', 'id_historia__quiero', 'n_horas').filter(
                id_historia__id_pbacklog__id_scrum=scrum)

    id_proyecto = Proyecto.objects.get(id=id_pro)

    contexto = {
                'historia': historia,
                'tareas': tareas,
                'id_proyecto': id_proyecto
            }

    datos = {'tabla_historias': render_to_string('clean/scrum/tabla_historias.html', contexto),
             'tabla_tareas': render_to_string('clean/scrum/tabla_tareas.html',
                                              {'tareas': tareas})
             }
    return JsonResponse(datos)


@login_required
def sbacklog_estado(request):

    form = SbacklogForm

    if request.method == 'POST':
        form = SbacklogForm(data=request.POST)
        if form.is_valid():
            sbacklog = Sbacklog()
            sbacklog.estado = form.cleaned_data['estado']
            sbacklog.save()
            return redirect('scrum:pbacklog_list')

    return redirect('scrum:pbacklog_list')


@login_required
def sprint(request, id):

    if request.method == 'POST':
        form = SprintForm(data=request.POST)
        if form.is_valid():
            form.save()
            requisito = form.cleaned_data['id_pbacklog']
            for r in requisito:
                Pbacklog.objects.filter(id=r.id).update(estado=False, confirmar=False)

            pro = request.POST['idIndex']
            request.session['proyectoIndex'] = pro
            return get_data(request, id)
            #return redirect('/proyecto/index2') #cambiar a path
    else:
        form = SprintForm

    proyecto_informacion = ProUser.objects.filter(proyecto=id).annotate(
        integrantes=Count('usuario'),
        numero_horas=Sum('horas')
    )

    integrantes = 0
    numero_horas = 0
    for i in proyecto_informacion:
        integrantes += i.integrantes
        numero_horas += i.numero_horas

    scrum = Scrum.objects.filter(proyecto=id)

    idscrum = scrum[0].id

    # Consultar si el pryecto ya tiene sprint creados
    try:
        dsprint = Sprint.objects.filter(id_scrum__proyecto=id).reverse()[0]
    except:
        dsprint = ""



    fecha = Proyecto.objects.values('f_inicio','f_fin').get(id=id)

    #sacar fechas y convertirlas a string
    if dsprint:
        fecha_inicio = datetime.strftime(dsprint.f_fin, '%Y-%m-%d')
    else:
        fecha_inicio = datetime.strftime(fecha['f_inicio'], '%Y-%m-%d')

    fecha_fin = datetime.strftime(fecha['f_fin'], '%Y-%m-%d')

    requisitos = Pbacklog.objects.filter(id_scrum=idscrum, confirmar=False).annotate(
        historias = Count('historiausuario__id'),
        historias_r = Count('historiausuario__id', filter=Q(historiausuario__estado=True)),
        tareas = Count('historiausuario__sbacklog__id'),
        tareas_r = Count('historiausuario__sbacklog__id', filter=Q(historiausuario__sbacklog__estado=True)),
        duracion = Sum('historiausuario__sbacklog__n_horas')
    ).order_by('id')
    contexto = {
        'form':form,
        'requisitos':requisitos,
        'idScrum':idscrum,
        'index':id,
        'fecha_inicio':fecha_inicio,
        'fecha_fin':fecha_fin,
        'numero_integrantes':integrantes,
        'numero_horas':numero_horas
    }
    return render(request, 'scrum/sprint_form.html', contexto)


@login_required
def dailymeeting(request):
    if request.method == 'POST':
        print(request.POST)

        ayer = request.POST['ayer']
        hoy = request.POST['hoy']
        problemas = request.POST['problemas']
        sp = request.POST['sprint']
        sprint = Sprint.objects.get(id=sp)
        us = request.user.pk
        usuario = User.objects.get(id=us)

        d = DailyMeeting.objects.create(ayer=ayer, hoy=hoy, problemas=problemas, sprint=sprint, usuario=usuario)
        d.save()

        return JsonResponse({'datos':'ready'})


@login_required
def sreview(request):
    if request.method == 'POST':
        id_proyecto = request.POST['id_proyecto']
        logros = request.POST['logros']
        id_pbacklog = request.POST['id_pbacklog'].split(',')
        observaciones = request.POST['observaciones']
        id_sprint = request.POST['sprint']

        sprint = Sprint.objects.get(id=id_sprint)
        form = Sreview.objects.create(logros=logros, observaciones=observaciones,sprint=sprint)
        print(request.POST)
        print('datos de requisitos',id_pbacklog)
        if id_pbacklog and id_pbacklog != ['']:
            for i in id_pbacklog:
               Pbacklog.objects.filter(id=i).update(estado=False, confirmar=True)
               p =  Pbacklog.objects.get(id=i)
               form.id_pbacklog.add(p)

        Sprint.objects.filter(estado=False, confirmar=True, id_scrum__proyecto__id=id_proyecto).update(confirmar=False)

    '''
    if request.method == 'POST':
        form = SreviewFrom(data=request.POST)

        print('datos enviados por post')
        print(request.POST)
        pro = request.POST['id_proyecto']
        observaciones = request.POST['observaciones']
        logros = request.POST['logros']
        requisitos = request.POST['id_pbacklog']
        print('requisitos')
        print(requisitos)
       # print(id_pbacklog)
        if form.is_valid():
            print('datos formulario')
            print(form.cleaned_data)

            #Pbacklog.objects.filter(id=r.id).update(estado=False, confirmar=True)

            #form.save()
            #Sprint.objects.filter(estado=False, confirmar=True, id_scrum__proyecto__id=pro).update(confirmar=False)
        else:
            print('error de datos')

        datos = {'datos':'enviados'}
        #print(requisitos)
    '''
    datos = {'datos': 'enviados'}
    return JsonResponse(datos)


@login_required
def update_pbacklog(request):
    if request.method == 'POST':
        id = request.POST['id_pbacklog']
        nombre = request.POST['nombre']
        sprint = request.POST['sprint']
        Pbacklog.objects.filter(id=id).update(nombre=nombre)
        p = Pbacklog.objects.filter(id_scrum=sprint, estado=False, confirmar=False).order_by('id')
        datos = {'tabla_sprint': render_to_string('clean/update_pbacklog_sprint.html',{'requisitos':p})}

    return JsonResponse(datos)


@login_required
def update_historia(request):
    if request.method == 'POST':
        id = request.POST['idh']
        nombre = request.POST['nombre']
        quiero = request.POST['quiero']
        para = request.POST['para']
        id_pro = request.POST['id_pro']

        HistoriaUsuario.objects.filter(id=id).update(como_usuario=nombre, quiero=quiero, para=para)
        scrum = request.session['scrum']

        historia = HistoriaUsuario.objects.filter(id_pbacklog__id_scrum=scrum).annotate(
            tarea=Count('sbacklog__id')
        ).order_by('id')

        tareas = Sbacklog.objects.values('id','nombre', 'id_historia__quiero', 'n_horas').filter(
            id_historia__id_pbacklog__id_scrum=scrum)

        id_proyecto = Proyecto.objects.get(id=id_pro)

        contexto = {
            'historia': historia,
            'tareas': tareas,
            'id_proyecto': id_proyecto
        }

        datos = {'tabla_historias': render_to_string('clean/scrum/tabla_historias.html',contexto),
                 'tabla_tareas': render_to_string('clean/scrum/tabla_tareas.html',
                                                  {'tareas': tareas})
                 }

    return JsonResponse(datos)


def update_epica(request):
    scrum = request.POST['scrum']
    if request.method == 'POST':
        id_pbacklog = request.POST['id_pbacklog']
        como_usuario = request.POST['nombre']
        quiero = request.POST['quiero']
        para = request.POST['para']

        Pbacklog.objects.filter(id=id_pbacklog).update(nombre=como_usuario, quiero=quiero, para=para)

    backlog = Pbacklog.objects.filter(id_scrum=scrum).annotate(
            hu=Count('historiausuario__id')
        ).order_by('id')

    datos = {'datos': render_to_string('clean/scrum/table_epicas.html', {'pbacklog': backlog, 'scrum':scrum})}
    return JsonResponse(datos)


def delete_epica(request):
    scrum = request.POST['scrum']
    if request.method == "POST":
        id = request.POST['id']
        Pbacklog.objects.filter(id=id).delete()

    backlog = Pbacklog.objects.filter(id_scrum=scrum).annotate(
        hu=Count('historiausuario__id')
    ).order_by('id')

    datos = {'datos': render_to_string('clean/scrum/table_epicas.html', {'pbacklog': backlog, 'scrum': scrum})}
    return JsonResponse(datos)


def delete_historia(request):
    id_pro = request.POST['id_pro']
    if request.method == "POST":
        id = request.POST['id']
        HistoriaUsuario.objects.filter(id=id).delete()

    scrum = request.session['scrum']

    historia = HistoriaUsuario.objects.filter(id_pbacklog__id_scrum=scrum).annotate(
        tarea=Count('sbacklog__id')
    ).order_by('id')

    tareas = Sbacklog.objects.values('id','nombre', 'id_historia__quiero', 'n_horas').filter(
        id_historia__id_pbacklog__id_scrum=scrum)

    id_proyecto = Proyecto.objects.get(id=id_pro)

    contexto = {
        'historia': historia,
        'tareas': tareas,
        'id_proyecto': id_proyecto
    }

    datos = {
        'tabla_historias': render_to_string('clean/scrum/tabla_historias.html', contexto),
        'tabla_tareas': render_to_string('clean/scrum/tabla_tareas.html',
                                              {'tareas': tareas})
    }
    return JsonResponse(datos)


@login_required
def eliminarPbacklog(request):

    id = request.GET['id']
    print('id que llega ', id)
    idscrum = Scrum.objects.get(pbacklog__id=id)
    requisitos = Pbacklog.objects.filter(id_scrum=idscrum.id, confirmar=False).annotate(
        historias=Count('historiausuario__id'),
        historias_r=Count('historiausuario__id', filter=Q(historiausuario__estado=True)),
        tareas=Count('historiausuario__sbacklog__id'),
        tareas_r=Count('historiausuario__sbacklog__id', filter=Q(historiausuario__sbacklog__estado=True)),
        duracion=Sum('historiausuario__sbacklog__n_horas')
    ).order_by('id')

    if request.method == 'GET':
        h = Pbacklog.objects.get(id=id)
        h.delete()

    contexto = {
        'requisitos': requisitos
    }

    datos = {
        'tabla_general': render_to_string('clean/scrum/tabla_epicas_general_sprint.html', {'requisitos': requisitos}),
        'tabla_editar_epica': render_to_string('clean/scrum/tabla_editar_epicas_sprint.html', {'requisitos': requisitos})
    }

    return JsonResponse(datos)


def delete_tarea(request):
    id_pro = request.GET['id_pro']
    if request.method == "GET":
        id = request.GET["id"]
        Sbacklog.objects.filter(id=id).delete()

    scrum = request.session['scrum']

    historia = HistoriaUsuario.objects.filter(id_pbacklog__id_scrum=scrum).annotate(
        tarea=Count('sbacklog__id')
    ).order_by('id')

    tareas = Sbacklog.objects.values('id', 'nombre', 'id_historia__quiero', 'n_horas').filter(
        id_historia__id_pbacklog__id_scrum=scrum)

    id_proyecto = Proyecto.objects.get(id=id_pro)

    contexto = {
        'historia': historia,
        'tareas': tareas,
        'id_proyecto': id_proyecto
    }

    datos = {
        'tabla_historias': render_to_string('clean/scrum/tabla_historias.html',
        contexto),
        'tabla_tareas': render_to_string('clean/scrum/tabla_tareas.html',
                                         {'tareas':tareas})
    }
    return JsonResponse(datos)


def edit_epica_sprint(request):
    id = request.POST['id']
    idscrum = Scrum.objects.get(pbacklog__id = id)

    if request.method == 'POST':
        nombre = request.POST['rol']
        quiero = request.POST['quiero']
        para = request.POST['para']

        Pbacklog.objects.filter(id=id).update(nombre=nombre, quiero=quiero, para=para)

   # datos = {'datos': render_to_string('clean/scrum/table_epicas.html', {'pbacklog': backlog, 'scrum':scrum})}

    requisitos = Pbacklog.objects.filter(id_scrum=idscrum.id, confirmar=False).annotate(
        historias=Count('historiausuario__id'),
        historias_r=Count('historiausuario__id', filter=Q(historiausuario__estado=True)),
        tareas=Count('historiausuario__sbacklog__id'),
        tareas_r=Count('historiausuario__sbacklog__id', filter=Q(historiausuario__sbacklog__estado=True)),
        duracion=Sum('historiausuario__sbacklog__n_horas')
    ).order_by('id')
    contexto = {
        'requisitos': requisitos
    }

    datos = {
        'tabla_general': render_to_string('clean/scrum/tabla_epicas_general_sprint.html', {'requisitos':requisitos}),
        'tabla_editar_epica': render_to_string('clean/scrum/tabla_editar_epicas_sprint.html', contexto)
    }

    return JsonResponse(datos)


def listado_historias_sprint(request):
    id = request.GET['id']
    historias = datos_sprint(id)

    contexto =  {
        'historias': historias['historias'],
        'id_pbacklog': id
    }
    datos = {
        'modulo_historia': render_to_string('clean/scrum/edicion_historias.html',contexto)
    }
    return JsonResponse(datos)


def editar_historia_sprint(request):

    if request.method == 'POST':

        id = request.POST['id']
        rol = request.POST['rol']
        quiero = request.POST['quiero']
        para = request.POST['para']
        
        HistoriaUsuario.objects.filter(id=id).update(como_usuario=rol,quiero=quiero,para=para)

        data = datos_sprint(request.POST['id_pbacklog'])
        mo_historia = data['modulo_historia']
        t_general = data['tabla_general']
        edit_epica = data['tabla_editar_epica']

        contexto = {
            'modulo_historia': mo_historia,
            'tabla_general': t_general,
            'tabla_editar_epica': edit_epica
        }
    return JsonResponse(contexto)


def eliminar_historia(request):

    if request.method == "GET":

        id = request.GET['id']
        idp = request.GET['idp']
        HistoriaUsuario.objects.filter(id=id).delete()

        data = datos_sprint(idp)
        mo_historia = data['modulo_historia']
        t_general = data['tabla_general']
        edit_epica = data['tabla_editar_epica']

        contexto = {
            'modulo_historia': mo_historia,
            'tabla_general': t_general,
            'tabla_editar_epica': edit_epica
        }
    return JsonResponse(contexto)


def tabla_tareas_sprint(request):
    idh = request.GET['idh']
    idp = request.GET['idp']
    tareas = Sbacklog.objects.filter(id_historia=idh)

    data = datos_sprint(idp)

    contexto = {
        'tareas_sprint': render_to_string('clean/scrum/tabla_tareas_sprint.html',{'tareas':tareas, 'id_historia':idh, 'id_pbacklog':idp})
    }

    return JsonResponse(contexto)


def datos_sprint(id):
    idscrum = Scrum.objects.get(pbacklog__id=id)
    requisitos = Pbacklog.objects.filter(id_scrum=idscrum.id, confirmar=False).annotate(
        historias=Count('historiausuario__id'),
        historias_r=Count('historiausuario__id', filter=Q(historiausuario__estado=True)),
        tareas=Count('historiausuario__sbacklog__id'),
        tareas_r=Count('historiausuario__sbacklog__id', filter=Q(historiausuario__sbacklog__estado=True)),
        duracion=Sum('historiausuario__sbacklog__n_horas')
    ).order_by('id')

    historias = HistoriaUsuario.objects.filter(id_pbacklog=id).annotate(
        tareas=Count('sbacklog__id')
    )

    contexto = {
        'requisitos': requisitos,
        'historias': historias,
        'tabla_general': render_to_string('clean/scrum/tabla_epicas_general_sprint.html', {'requisitos': requisitos}),
        'tabla_editar_epica': render_to_string('clean/scrum/tabla_editar_epicas_sprint.html', {'requisitos': requisitos}),
        'modulo_historia': render_to_string('clean/scrum/edicion_historias.html', {'historias':historias, 'id_pbacklog': id})
    }

    return contexto


def add_tarea_sprint(request):
    if request.method == "POST":
        sback = SbacklogForm(data=request.POST)
        if sback.is_valid():
            sback.save()

    idp = request.POST['id_pbacklog']
    data = datos_sprint(idp)
    mo_historia = data['modulo_historia']
    t_general = data['tabla_general']
    edit_epica = data['tabla_editar_epica']

    idh = request.POST['id_historia']

    tareas = Sbacklog.objects.filter(id_historia=idh)

    contexto = {
        'modulo_historia': mo_historia,
        'tabla_general': t_general,
        'tabla_editar_epica': edit_epica,
        'tareas_sprint': render_to_string('clean/scrum/tabla_tareas_sprint.html',
                                          {'tareas': tareas, 'id_historia': idh, 'id_pbacklog': idp})
    }

    return JsonResponse(contexto)


def update_tarea_sprint(request):

    if request.method == "POST":
        id = request.POST['id']

        descripcion = request.POST['nombre']
        duracion = request.POST['n_horas']
        Sbacklog.objects.filter(id=id).update(nombre = descripcion, n_horas=duracion)

    idp = request.POST['idp']
    data = datos_sprint(idp)
    mo_historia = data['modulo_historia']
    t_general = data['tabla_general']
    edit_epica = data['tabla_editar_epica']
    idh = request.POST['idh']
    tareas = Sbacklog.objects.filter(id_historia=idh)

    contexto = {
        'modulo_historia': mo_historia,
        'tabla_general': t_general,
        'tabla_editar_epica': edit_epica,
        'tareas_sprint': render_to_string('clean/scrum/tabla_tareas_sprint.html',
                                          {'tareas': tareas, 'id_historia': idh, 'id_pbacklog': idp})
    }

    return JsonResponse(contexto)