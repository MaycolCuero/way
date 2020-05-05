from django import forms
from apps.proyecto.models import Proyecto

class ProyectoForm(forms.ModelForm):

    class Meta:
        model = Proyecto

        fields = [
            'nombre',
            'f_inicio',
            'f_fin',
            'id_metodologia',
        ]

        labels = {
            'nombre': 'Nombre del proyecto',
            'f_inicio': 'Fecha de inicio',
            'f_fin': 'Fecha de fin',
            'id_metodologia':'Métodologia de desarrollo',
        }

        widgets = {
           'nombre': forms.TextInput(attrs={
               'class':'form-control',
               'required': 'required'
           }),

            'f_inicio': forms.DateInput(attrs={
                'class':'form-control',
                'type':'date',
                'required':'required'
            }),

            'f_fin': forms.DateInput(attrs={
                'class':'form-control',
                'type':'date',
                'required': 'required'
                 }),

            'id_metodologia': forms.TextInput(attrs={'class':'form-control'}),
            #'usuario': forms.HiddenInput(),
        }
