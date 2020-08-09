from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.db.models import Count, Q, Sum
from django.views.generic import View, CreateView, UpdateView, ListView, DetailView

from apps.xp.models import XP, Ciclo
from apps.xp.forms import HistoriaUsuarioXPForm
from apps.scrum.models import HistoriaUsuario, Sbacklog
from apps.scrum.forms import SbacklogForm
from apps.proyecto.models import ProUser, Proyecto, Rol
from apps.usuarios.models import User
from datetime import datetime
# Create your views here.


class CrearHistorias(View):
    model = HistoriaUsuario
    form_class = HistoriaUsuarioXPForm
    template_name = 'xp/historia_usuario.html'
    #success_url = reverse_lazy('usuarios:index')

    def get_context_data(self,*args):
        h = HistoriaUsuario.objects.filter(id_xp=args[1]).annotate(
            tareas=Count('sbacklog__id')
        )
        t = Sbacklog.objects.values('id_historia__quiero','nombre','n_horas').filter(id_historia__id_xp=args[1])
        xp = args[1]
        id_pro = XP.objects.values('proyecto').get(id=xp)
        contexto = {
            'form':self.form_class,
            'historias':h,
            'xp':xp,
            'tareas':t,
            'id_pro':id_pro['proyecto']
        }
        return contexto

    def get(self,request,*args,**kwargs):
        xp = request.session['xp']
        return render(request,self.template_name,self.get_context_data(self,xp))

    def post(self, request,*args, **kwargs):
        form = self.form_class(request.POST)
        print('datos del formularaio',form)
        if form.is_valid():
            form.save()

        return redirect('xp:CrearHistorias')


def index(request, id):
    task = Sbacklog.objects.filter(
        id_historia__get = True,
        id_historia__id_ciclo__id_xp__proyecto=id,
        estado=False,
        get=False
    )

    requisitos = HistoriaUsuario.objects.filter(
        id_xp__proyecto__id=id,
        get=True,
        id_ciclo__estado=True,
        id_ciclo__id_xp__proyecto=id,
        estado=False
    )

    proceso = Sbacklog.objects.filter(
        id_historia__get = True,
        id_historia__id_ciclo__id_xp__proyecto=id,
        estado=False,
        get=True
    )


    historias = HistoriaUsuario.objects.filter(id_xp__proyecto__id=id, get=False).annotate(
        dias=Sum('sbacklog__n_horas'),
        tareas=Count('sbacklog__id')
    )

    terminadas = Sbacklog.objects.filter(
        estado=True,
        id_historia__id_ciclo__id_xp__proyecto=id,
        id_historia__id_ciclo__estado=True
    )

    integrantes = User.objects.values('id','first_name','last_name').filter(prouser__proyecto=id)


    xp = XP.objects.values('id','proyecto__id','proyecto__nombre','proyecto__f_inicio','proyecto__f_fin').get(proyecto=id)

    resumen_pro = resumen(id)

    resumen_proyecto = resumen_pro['proyecto']
    resumen_historias = resumen_pro['historias']
    resumen_tareas = resumen_pro['tareas']
    resumen_integrantes = resumen_pro['integrantes']
    resumen_ciclo = resumen_pro['ciclo']
    resumen_ciclo_historias = resumen_pro['ciclo_historias']
    try:
        ciclo = Ciclo.objects.get(id_xp__proyecto=id,estado=True)
    except:
        ciclo = ""

    xp_f_inicio = datetime.strftime(xp['proyecto__f_inicio'], '%Y-%m-%d')
    xp_f_fin =  datetime.strftime( xp['proyecto__f_fin'], '%Y-%m-%d')

    print('inicio: ',xp_f_inicio, ' fin :',xp_f_fin)


    contexto = {
        'requisitos':requisitos,
        'xp':xp,
        'pendientes':task,
        'historias': historias,
        'integrantes':integrantes,
        'procesos':proceso,
        'terminadas':terminadas,
        'ciclo':ciclo,
        'resumen_proyecto':resumen_proyecto,
        'resumen_historias':resumen_historias,
        'resumen_tareas':resumen_tareas,
        'resumen_integrantes':resumen_integrantes,
        'resumen_ciclo':resumen_ciclo,
        'resumen_ciclo_historias':resumen_ciclo_historias,
        'id_pro':id,
        'xp_f_inicio': xp_f_inicio,
        'xp_f_fin': xp_f_fin
    }

    return render(request, 'xp/index-xp.html', contexto)


class CrearTareas(CreateView):
    model = Sbacklog
    form_class = SbacklogForm
    template_name = 'xp/historia_usuario.html'
    success_url = reverse_lazy('xp:CrearHistorias')


class ActualizarHistorias(UpdateView):
    model = HistoriaUsuario
    form_class = HistoriaUsuarioXPForm
    template_name = 'xp/actualizar_historia.html'
    success_url = reverse_lazy('xp:CrearHistorias')


def eliminarHistoria(request, id):
    if request.method == 'GET':
        h = HistoriaUsuario.objects.get(id=id)
        h.delete()
    return redirect('xp:CrearHistorias')


def crearCiclo(request):
    #Todos los derechos reservados por Maycol Cuero Ruiz

    if request.method == "POST":
        f_inicio = request.POST['f_inicio']
        f_fin = request.POST['f_fin']
        id_xp = request.POST['id_xp']
        id_historia = request.POST['idh'].split(',')

        xp = XP.objects.get(id=id_xp)
        #Crear Ciclo
        ciclo = Ciclo.objects.create(f_inicio=f_inicio,f_fin=f_fin,estado=True, id_xp=xp)
        if id_historia and id_historia != ['']:
            for h in id_historia:
                HistoriaUsuario.objects.filter(id=h).update(id_ciclo=ciclo.id, get=True)

    return JsonResponse({'datos':'resividos'})


def integrante_historia(request):
    if request.method == "POST":
        id_historia = request.POST['id_historia']
        id_usuario = request.POST['id_usuario']

    return JsonResponse('datos enviados')


def agregar_integrantes(request):
    if request.method == "POST":
        proyecto = request.POST['idpro']
        email = request.POST['email']
        rol = request.POST['rol']
        dato = "SI"
        us = "SI" #ayuda a verificar si el usuario ya existe
        try:
            usuario = User.objects.get(email=email)
        except:
            dato ="NO"

        if dato == "SI":
            u = ProUser.objects.filter(proyecto=proyecto, usuario=usuario.id)
            if u:
                us = "SI"
            else:
                us = "NO"

        if dato == "SI" and us == "NO":
            idpro = Proyecto.objects.get(id=proyecto)
            rol = Rol.objects.get(nombre=rol)
            ProUser.objects.create(proyecto=idpro, usuario = usuario, rol = rol)
            integrantes = User.objects.values('id', 'first_name', 'last_name').filter(prouser__proyecto=idpro.id)
            datos = {'datos_integrantes': render_to_string('clean/xp/integrantes.html', {'integrantes': integrantes})}
            return JsonResponse(datos)
        else:
            dato = "NO"
            return JsonResponse({'datos':dato})


def datos_actualizacion_tabla(id):
    task = Sbacklog.objects.filter(
        id_historia__get=True,
        id_historia__id=id,
        estado=False,
        get=False
    )
    proyecto = Proyecto.objects.get(xp__historiausuario__id=id)

    requisitos = HistoriaUsuario.objects.filter(
        id_xp__proyecto__id=proyecto.id,
        get=True,
        id_ciclo__estado=True,
        id_ciclo__id_xp__proyecto=proyecto.id,
        estado=False
    )

    proceso = Sbacklog.objects.filter(
        id_historia__get=True,
        id_historia__id=id,
        estado=False,
        get=True
    )

    historias = HistoriaUsuario.objects.filter(id=id, get=False).annotate(
        dias=Sum('sbacklog__n_horas'),
        tareas=Count('sbacklog__id')
    )

    terminadas = Sbacklog.objects.filter(
        estado=True,
        id_historia__id=id,
        id_historia__id_ciclo__estado=True
    )

    contexto = {
        'requisitos': requisitos,
        'pendientes': task,
        'historias': historias,
        'procesos': proceso,
        'terminadas': terminadas
    }

    return contexto


def obtener(request):
    if request.method == "GET":
        id = request.GET['id_tarea']
        u = request.user.pk
        Sbacklog.objects.filter(id=id).update(usuario=u, get=True, estado=False)
        historia = HistoriaUsuario.objects.get(sbacklog__id=id)

        contexto = datos_actualizacion_tabla(historia.id)


    datos = {'tabla_xp': render_to_string('clean/xp/tabla.html', contexto)}
    return JsonResponse(datos)


def confirmar(request):
    id = request.GET['id_tarea']

    Sbacklog.objects.filter(id=id).update(estado=True)

    # Consulto la historia de usuario
    h = HistoriaUsuario.objects.filter(sbacklog__id=id)

    # calculo si las tareas perteneciente a la misma historia de usuarios q ya estan completadas
    a = Sbacklog.objects.filter(id_historia=h[0].id).count()
    b = Sbacklog.objects.filter(id_historia=h[0].id, estado=True).count()

    # obtengo el procentaje de tareas cumplidas y dependiendo del resultado actualizo el modelo HistoriaUsuario
    x = (b * 100) / a
    if x == 100:
        HistoriaUsuario.objects.filter(id=h[0].id).update(estado=True)

    ciclo = Ciclo.objects.get(historiausuario__id=h[0].id)

    historias_ciclo = HistoriaUsuario.objects.filter(id_ciclo=ciclo.id).count()
    hcp = HistoriaUsuario.objects.filter(id_ciclo=ciclo.id,estado=True).count()

    hr = (hcp * 100) / historias_ciclo

    if hr == 100:
        Ciclo.objects.filter(id=ciclo.id).update(estado=False)

    datos = datos_actualizacion_tabla(h[0].id)

    info = {'tabla_xp': render_to_string('clean/xp/tabla.html', datos)}
    return JsonResponse(info)


def resumen(id_proyecto):

    xp = XP.objects.values('id', 'proyecto__id', 'proyecto__nombre', 'proyecto__f_inicio', 'proyecto__f_fin').get(
        proyecto=id_proyecto)

    historias = HistoriaUsuario.objects.filter(id_xp__proyecto__id=id_proyecto).annotate(
        dias=Sum('sbacklog__n_horas'),
        tareas=Count('sbacklog__id')
    )

    task = Sbacklog.objects.values(
        'id',
        'nombre',
        'usuario__first_name',
        'usuario__last_name',
        'n_horas',
        'id_historia__id_ciclo'
    ).filter(
        id_historia__get=True,
        id_historia__id_ciclo__id_xp__proyecto=id_proyecto
    )

    ciclo = Ciclo.objects.filter(id_xp__proyecto=id_proyecto)
    ciclo_historias = HistoriaUsuario.objects.filter(id_xp__proyecto__id=id_proyecto)

    integrantes = ProUser.objects.values(
        'usuario__first_name',
        'usuario__last_name',
        'rol__nombre'
    ).filter(proyecto=id_proyecto)

    contexto = {
        'proyecto':xp,
        'historias':historias,
        'tareas':task,
        'integrantes':integrantes,
        'ciclo':ciclo,
        'ciclo_historias':ciclo_historias
    }

    return contexto

def update_history(request):
    if request.method == 'GET':
        id_pro = request.GET['id_pro']
        historias = HistoriaUsuario.objects.filter(id_xp__proyecto__id=id_pro).annotate(
            dias=Sum('sbacklog__n_horas'),
            tareas=Count('sbacklog__id')
        )
        contexto = {
            'id_pro':id_pro,
            'historias':historias
        }
        datos = {'update_history':render_to_string('clean/xp/update_history.html',contexto)}

    return JsonResponse(datos)


def show_crear_ciclo(request):
    if request.method == 'GET':
        id_pro = request.GET['id_pro']
        historias = HistoriaUsuario.objects.filter(id_xp__proyecto__id=id_pro, get=False).annotate(
            dias=Sum('sbacklog__n_horas'),
            tareas=Count('sbacklog__id')
        )

        xp = XP.objects.values('id','proyecto__id','proyecto__nombre','proyecto__f_inicio','proyecto__f_fin').get(proyecto=id_pro)
        xp_f_inicio = datetime.strftime(xp['proyecto__f_inicio'], '%Y-%m-%d')
        xp_f_fin =  datetime.strftime( xp['proyecto__f_fin'], '%Y-%m-%d')

        contexto = {
            'id_pro':id_pro,
            'historias':historias,
            'xp':xp,
            'xp_f_inicio': xp_f_inicio,
            'xp_f_fin': xp_f_fin
        }
        datos = {'show_crear_ciclo':render_to_string('clean/xp/show_crear_ciclo.html',contexto)}

    return JsonResponse(datos)

def add_history_ciclo(request):
    idpro = request.POST['id_pro']
    if request.method == "POST":
        
        xp = XP.objects.get(proyecto__id=idpro)
        usuario = request.POST['como_usuario']
        quiero = request.POST['quiero']
        para = request.POST['para']
        history = HistoriaUsuario.objects.create(como_usuario=usuario,
            quiero=quiero,
            para= para,
            estado = False,
            get = False,
            id_xp = xp
        )

    
    data = datos_ciclo(idpro)
    historia = data['update_history']

    contexto = {
        'update_history':historia
    }
       
       
    return JsonResponse(contexto)


def datos_ciclo(id):
    task = Sbacklog.objects.filter(
        id_historia__get = True,
        id_historia__id_ciclo__id_xp__proyecto=id,
        estado=False,
        get=False
    )

    requisitos = HistoriaUsuario.objects.filter(
        id_xp__proyecto__id=id,
        get=True,
        id_ciclo__estado=True,
        id_ciclo__id_xp__proyecto=id,
        estado=False
    )

    proceso = Sbacklog.objects.filter(
        id_historia__get = True,
        id_historia__id_ciclo__id_xp__proyecto=id,
        estado=False,
        get=True
    )


    historias = HistoriaUsuario.objects.filter(id_xp__proyecto__id=id, get=False).annotate(
        dias=Sum('sbacklog__n_horas'),
        tareas=Count('sbacklog__id')
    )

    terminadas = Sbacklog.objects.filter(
        estado=True,
        id_historia__id_ciclo__id_xp__proyecto=id,
        id_historia__id_ciclo__estado=True
    )

    integrantes = User.objects.values('id','first_name','last_name').filter(prouser__proyecto=id)


    xp = XP.objects.values('id','proyecto__id','proyecto__nombre','proyecto__f_inicio','proyecto__f_fin').get(proyecto=id)
    xp_f_inicio = datetime.strftime(xp['proyecto__f_inicio'], '%Y-%m-%d')
    xp_f_fin =  datetime.strftime( xp['proyecto__f_fin'], '%Y-%m-%d')

    datos = {
        'update_history':render_to_string('clean/xp/update_history.html',{'id_pro':id,
            'historias':historias}),
        'show_crear_ciclo':render_to_string('clean/xp/show_crear_ciclo.html',{
            'id_pro':id,
            'historias':historias,
            'xp':xp,
            'xp_f_inicio': xp_f_inicio,
            'xp_f_fin': xp_f_fin
        })
    }

    return datos