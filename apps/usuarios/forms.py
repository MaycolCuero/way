from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import widgets

from apps.usuarios.models import Usuario
from django import forms


class RegistroForm(forms.Form):
    first_name = forms.CharField(label='Nombre', max_length=100,
                                 widget=forms.TextInput(attrs={
                                         'class':'form-control form-control-user',
                                         'placeholder':'Nombres',
                                     }
                                 ))

    username = forms.CharField(label='Nombre de usuario', max_length=100,
                                 widget=forms.TextInput(attrs={
                                         'class':'form-control form-control-user',
                                         'placeholder':'Nombre de usuario',
                                     }
                                 ))

    last_name = forms.CharField(label='Apellidos', max_length=100,
                                widget=forms.TextInput(attrs={
                                        'class': 'form-control form-control-user',
                                        'placeholder': 'Apellidos',
                                    }
                                ))

    email = forms.EmailField(label='Email',  widget=forms.EmailInput(attrs={
                                         'class':'form-control form-control-user',
                                         'placeholder':'Correo electrónico',
                                     }
                                 ))

    password = forms.CharField(label='Contraseña',
                               strip=False,
                               widget=forms.PasswordInput(attrs={
                                         'class':'form-control form-control-user',
                                         'placeholder':'Contraseña',
                                     }
                                 ))

    #photo = forms.ImageField(label='Imagen de perfil')

    def registrarusario(self, User):
        '''
        usuario = User(first_name=datos['first_name'],
                       last_name=datos['last_name'],
                       username=datos['username'],
                       email=datos['email'],
                       password=datos['password'])
        usuario.save()
        '''

        return 'Registro exitoso'


'''
class LoginForm(forms.ModelForm):

    class Meta:
        model = User

        fields = [
            'username',
            'password',
        ]

        labels = {
            'username':'Nombre de Usuario',
            'password': 'Contraseña',
        }

        widgets = {
            'username': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Ingrese nombre de usuario',
            }),
            'password': forms.PasswordInput(attrs={
                'class':'form-control',
                'placeholder':'Ingrese su contraseña',
            }),
        }
'''


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Ingrese su nombre de usuario'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Ingrese su contraseña'


class UsuarioForm(forms.ModelForm):

   class Meta:

       model = Usuario

       fields = [
           'celular',
           'id_user',
           'photo',
       ]

       labels = {
           'celular': 'Número de celular',
           'photo': 'Foto de perfil',
       }