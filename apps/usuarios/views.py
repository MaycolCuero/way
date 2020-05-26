'''
    repositorio de github donde se encuntra el tutorial para cambiar la contraseña
    https://github.com/CoreyMSchafer/code_snippets/tree/master/Django_Blog/12-Password-Reset/django_project
'''


import json

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login, logout as do_logout
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView
from django.utils.decorators import method_decorator #decorador que se utiliza para aumentar la seguridad
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login

from apps.usuarios.forms import RegistroForm, UsuarioForm, LoginForm
from apps.scrum.models import HistoriaUsuario, Pbacklog, Sbacklog, Scrum, Sprint
from django.db.models import Count, Q, Sum
from apps.usuarios.models import User, Usuario
from apps.proyecto.models import Proyecto



@login_required
def index(request):
    id = request.user.pk
    requisitos = Count('scrum__pbacklog__id', filter=Q(usuario=id))
    rcompletados = Count('scrum__pbacklog__id', filter=Q(scrum__pbacklog__confirmar=True))

    # proyecto con scrum
    p = Proyecto.objects.values(
        'nombre',
        'id_metodologia__nombre',
        'id'
    ).filter(usuario=id, id_metodologia__nombre='SCRUM').annotate(
        requisitos=requisitos,
        rcompletados=rcompletados,
        num=((rcompletados * 100)/requisitos)
    )

    rpendientes_xp = Count('scrum__pbacklog__id', filter=Q(usuario=id))
    rcompletos_xp = Count('scrum__pbacklog__id', filter=Q(scrum__pbacklog__confirmar=True))
    #proyecto con xp
    xp_p = Proyecto.objects.values(
        'nombre',
        'id_metodologia__nombre',
        'id'
    ).filter(usuario=id, id_metodologia__nombre='XP').annotate(
        rpendientes=rpendientes_xp,
        rcompletados=rcompletos_xp
    )

    contexto = {'proyecto': p, 'xp_p':xp_p}

    return render(request, 'usuarios/index.html', contexto)

class Login(FormView):
    '''
        guia para la creacion de login
         https://www.youtube.com/watch?v=Twv0Ok9MerI
    '''
    template_name = 'usuarios/login2.html'
    form_class = LoginForm
    success_url = reverse_lazy('usuarios:index')


    #vamos a importar un decorador para un metodo, el cual nos ayudara a aumentar la seguridad
    #son dos never chache la cual evitara a que se guarden las credenciales en cache y crops.. que brinda seguridad a bulnerabilidades mas conocidas

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)

    #dispatch en vistas basadas en clases es el primero que se ejecuta, este metodo se encarga de redirigir las peticiones es decir si es POST la envia al metodo POST y si es GET la envia al GET
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            #return HttpResponseRedirect(self.get_success_url()) #el metodo get_success_url lo que hace es redireccionarnos a la direccion que especificamos arriba en este caso seria index
            return HttpResponseRedirect(self.get_success_url()) #el metodo get_success_url lo que hace es redireccionarnos a la direccion que especificamos arriba en este caso seria index
        else:
            return super(Login,self).dispatch(request, *args, **kwargs)

    def form_valid(self, form): # validamos el formulario de que se utiliza en la vista
        login(self.request, form.get_user())
        return super(Login,self).form_valid(form)


def logout(request):
    # finalizamos la sesion
    do_logout(request) #cierra todas las sesiones que se encuentren en el navegador, es decir borra los registros de la variblea request.session
    # Redireccionamos al login
    return redirect('usuarios:login')


def registrarusario(self):
    usuario = User(first_name=self.data['first_name'],
                   last_name=self.data['last_name'],
                   username=self.data['username'],
                   email=self.data['email'],
                   password=self.data['password1'])

    usuario.save()


def register(request):
    form = RegistroForm()

    if request.POST:

        usuario = User()
        usuario.first_name = request.POST['first_name']
        usuario.last_name = request.POST['last_name']
        usuario.username = request.POST['username']
        usuario.email = request.POST['email']
        usuario.password = request.POST['password']

        usercomplement = Usuario()
        usercomplement.photo = request.FILES.get('photo')
        usercomplement.celular = request.POST['celular']

        print('datos del usuario', usuario.first_name)
        print('datos del usuario', usuario.last_name)
        print('datos del usuario', usuario.username)
        print('datos del usuario', usuario.email)
        print('datos del usuario', usuario.password)
        print('datos de complemento', usercomplement.photo)
        print('datos de complemento', usercomplement.celular)



        usuario.save()

        usercomplement.id_user = usuario

        print('datos al guardar usuario',usuario)
        usercomplement.save()


    return render(request, "usuarios/register.html", {'form': form})

''''
def register(request):
    if request.method == "POST":
        print(request.POST, request.FILES)

        form = RegistroForm(request.POST)
        
        if form.is_valid():

            nomrbe = form.cleaned_data['first_name']
            apellido = form.cleaned_data['last_name']
            usuario = form.cleaned_data['username']
            correo = form.cleaned_data['email']
            passwd = form.cleaned_data['password']
            photo = request.FILES['photo']

           
            try:
                datos = User.objects.create_user(first_name=nomrbe, last_name=apellido, username=usuario, email=correo,
                                                 password=passwd)
                datos.save()

                if request.POST['celular'] != "":
                    cell = Usuario.objects.create(celular=request.POST['celular'], id_user=datos, photo=photo)
                    cell.save()
                return redirect('usuarios:login')
            except Exception as error:
                print("error", error)
           
        else:

            form = RegistroForm
    return render(request, "usuarios/register.html", {'form': form})
'''

def update(request):
    pass


@login_required
def perfil(request):
    usuario = User.objects.values('first_name','last_name', 'email', 'usuario__celular', 'username').filter(id=request.user.pk)
    proyecto = Proyecto.objects.filter(usuario=request.user.pk)
    contexto = {'contexto': usuario, 'proyecto': proyecto}
    return render(request, 'usuarios/perfil.html', contexto)


@login_required
def tareas(request):
    id = request.user.pk

    requisitos = Count('scrum__pbacklog__historiausuario__sbacklog__id',
                       filter=Q(scrum__pbacklog__historiausuario__sbacklog__estado=False,
                                scrum__pbacklog__historiausuario__sbacklog__get=True,
                                scrum__pbacklog__historiausuario__sbacklog__usuario=id
                                ))

    rcompletados = Count('scrum__pbacklog__id', filter=Q(scrum__pbacklog__estado=True))
    p = Proyecto.objects.values(
        'nombre',
        'id'
    ).filter(usuario=id).annotate(
        requisitos=requisitos,
        rcompletados=rcompletados
    )
    #contexto = {'tareas': tarea, 'proyecto': proyecto, 'hechas': hechas}
    contexto = {'proyecto': p}
    return render(request, 'usuarios/tareas.html', contexto)


@login_required
def confirmar(request):
    id = request.POST['id']
    Sbacklog.objects.filter(id=id).update(estado=True)

    # Consulto la historia de usuario
    h = HistoriaUsuario.objects.filter(sbacklog__id=id)
    pb = Pbacklog.objects.get(historiausuario__sbacklog__id=id)

    # calculo si las tareas perteneciente a la misma historia de usuarios q ya estan completadas
    a = Sbacklog.objects.filter(id_historia=h[0].id).count()
    b = Sbacklog.objects.filter(id_historia=h[0].id, estado=True).count()

    # obtengo el procentaje de tareas cumplidas y dependiendo del resultado actualizo el modelo HistoriaUsuario
    x = (b * 100) / a
    if x == 100:
        HistoriaUsuario.objects.filter(id=h[0].id).update(estado=True)

    # si todas las historias de usuarios de un requisito ya estan completadas le cambio el estado a verdadero
    h1 = HistoriaUsuario.objects.filter(id_pbacklog=pb.id).count()
    h2 = HistoriaUsuario.objects.filter(id_pbacklog=pb.id, estado=True).count()

    s = (h2 * 100) / h1
    if s == 100:
        Pbacklog.objects.filter(id=pb.id).update(estado=True)

    #si todos los requisitps seleccionados para un sprint ya estan cumplidos, desactivo el sprint par poder crear uno nuevo
    #par amayor presision utilizo el id de scrum para poder identificar exactamente el sprint perteneciente al proyecto
    idscrum = Scrum.objects.get(pbacklog__id=pb.id)
    idsprint = Sprint.objects.get(id_scrum=idscrum.id, estado=True)
    idpb = Pbacklog.objects.filter(sprint=idsprint).count()
    idpb_activo = Pbacklog.objects.filter(sprint=idsprint, estado=True).count()
    resultado = (idpb_activo * 100)/idpb
    if resultado == 100:
        Sprint.objects.filter(id=idsprint.id).update(estado=False, confirmar=True)
        #la variable confirmar en sprint sirve para que despues de terminado el sprint, se pueda avilitar el sprint review
    return JsonResponse({'datos':'guardados'})


@login_required
def getTareas(request):
    if request.method == 'GET':
        id = request.GET['id']
        usuario = request.user.pk
        d = Sbacklog.objects.filter(id_historia__id_pbacklog__id_scrum__proyecto__id=id, usuario=usuario, get=True, estado=False)
        datos = serializers.serialize('json', d)
    else:
        print("hubo algun error...")
    return HttpResponse(datos, content_type='application/json')


@login_required
def getTareasHechas(request):
    if request.method == 'GET':
        id = request.GET['id']
        usuario = request.user.pk
        h = Sbacklog.objects.filter(id_historia__id_pbacklog__id_scrum__proyecto__id=id, usuario=usuario, estado=True)
        hechas = serializers.serialize('json', h)
    else:
        print("hubo algun error...")

    return HttpResponse(hechas, content_type='application/json')