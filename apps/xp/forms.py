from django import forms

from apps.scrum.models import HistoriaUsuario, Sbacklog


class HistoriaUsuarioXPForm(forms.ModelForm):
    class Meta:
        model = HistoriaUsuario

        fields = ['como_usuario', 'quiero', 'para', 'estado','id_xp','get']

        labels = {
            'como_usuario':'Perfil del Usuario',
            'quiero':'Requisito del usuario',
            'para':'Objectivo del requisito',
        }

        widgets = {
            'como_usuario':forms.TextInput(attrs={
                'class':'form-control',
            }),
            'quiero':forms.Textarea(attrs={
                'class':'form-control',
                'rows': '2',
            }),
            'para': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '2',
            }),
            'id_xp':forms.TextInput(attrs={
                'type':'hidden'
            })
        }