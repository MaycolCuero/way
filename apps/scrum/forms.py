from django import forms
from apps.scrum.models import Scrum, Pbacklog, Sbacklog, HistoriaUsuario, Sprint, Sreview


class ScrumForm(forms.ModelForm):

    class Meta:
        model = Scrum

        fields = [
            'proyecto',
        ]

        labels = {
            'proyecto': 'Nombre del proyecto',
        }

        widgets = {
            'proyecto': forms.Select(attrs={'class':'form-control'}),
         }


class PbacklogForm(forms.ModelForm):
    class Meta:
        model = Pbacklog
        fields = [
            'nombre',
            'quiero',
            'para',
            'id_scrum',
            'estado',
            'confirmar',
        ]
        labels = {
            'nombre':'Nombre',
            'id_scrum':'Scrum',
            'estado':'estado',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'id_scrum': forms.Select(attrs={'class':'form-control'}),
        }


class HistoriaUsuarioForm(forms.ModelForm):

    class Meta:
        model = HistoriaUsuario

        fields = [
            'como_usuario',
            'quiero',
            'para',
            'estado',
            'id_pbacklog',
        ]

        labels = {
            'como_usuario': 'Como usuario',
            'quiero': 'Quiero',
            'estado': 'Estado de la historia',
            'para': 'Para',
            'id_pbacklog':'Product backlog',
        }

        widgets = {
            'como_usuario': forms.TextInput(attrs={'class':'form-control', 'required':'required'}),
            'quiero': forms.TextInput(attrs={'class':'form-control', 'required':'required'}),
            'estado': forms.TextInput(attrs={'class':'form-control', 'required':'required'}),
            'para': forms.Textarea(attrs={'class':'form-control', 'required':'required'}),
            'id_pbacklog': forms.Select(attrs={'class':'form-control'})
        }


class SbacklogForm(forms.ModelForm):

    class Meta:
        model = Sbacklog

        fields = [
            'nombre',
            'n_horas',
            'get',
            'estado',
            'id_historia',
        ]

        labels = {
            'nombre': 'Descripcion',
            'n_horas': 'Numero de horas',
            'id_historia': 'Historia',
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'get': forms.TextInput(attrs={'class':'form-control'}),
            'estado': forms.TextInput(attrs={'class':'form-control'}),
            'n_horas': forms.Select(),
            'id_historia': forms.Select(),
        }


class SprintForm(forms.ModelForm):

    class Meta:
        model = Sprint

        fields = ['f_inicio', 'f_fin','id_scrum','id_pbacklog','estado', 'confirmar']

        labels = {
            'f_inicio':'Fecha de inicio',
            'f_fin':'Fecha de finalización',
            'id_scrum':'Proyecto de scrum',
            'id_pbacklog':'lista de requisitos',
            'estato':'estado'
        }


class SreviewFrom(forms.ModelForm):

    class Meta:
        model = Sreview

        fields = ['logros','observaciones','sprint','id_pbacklog']

        labels = {
            'logros':'logros alcanzados',
            'observaciones':'observaciones Obtenidas',
        }
