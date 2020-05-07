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

    terminadas = Sbacklog.objects.filter(id_historia__id_xp__proyecto__id=id, estado=True)

    integrantes = User.objects.values('id','first_name','last_name').filter(prouser__proyecto=id)


    xp = XP.objects.values('id','proyecto__id','proyecto__nombre','proyecto__f_inicio','proyecto__f_fin').get(proyecto=id)
    try:
        ciclo = Ciclo.objects.get(id_xp__proyecto=id,estado=True)
    except:
        ciclo = ""
    contexto = {
        'requisitos':requisitos,
        'xp':xp,
        'pendientes':task,
        'historias': historias,
        'integrantes':integrantes,
        'procesos':proceso,
        'terminadas':terminadas,
        'ciclo':ciclo
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
        print('datos del formulario del ciclo',request.POST)

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
            rol = Rol.objects.get(id=rol)
            ProUser.objects.create(proyecto=idpro, usuario = usuario, rol = rol)
            integrantes = User.objects.values('id', 'first_name', 'last_name').filter(prouser__proyecto=idpro.id)
            datos = {'datos_integrantes': render_to_string('clean/xp/integrantes.html', {'integrantes': integrantes})}
            return JsonResponse(datos)
        else:
            dato = "NO"
            return JsonResponse({'datos':dato})

def obtener(request):
    if request.method == "GET":
        id = request.GET['id_tarea']
        u = request.user.pk
        Sbacklog.objects.filter(id=id).update(usuario=u, get=True, estado=False)

    return JsonResponse({'datos':'guardados'})

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

    return JsonResponse({'datos': 'guardados'})