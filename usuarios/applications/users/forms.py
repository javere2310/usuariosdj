from typing import Any, Mapping, Optional, Type, Union
from django import forms
from django.contrib.auth import authenticate
from django.forms.utils import ErrorList

from .models import User

class UserRegisterForm(forms.ModelForm):
    
    password1 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña'
            }
        )
    )

    password2 = forms.CharField(
        label='Repetir Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Repetir Contraseña'
            }
        )
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'nombres',
            'apellidos',
            'genero',
        )

    # función "clean_campox", indica a django hay una validación en el campo especificado
    def clean_password2(self):
        # print('password1', self.cleaned_data["password1"])
        # print('password2', self.cleaned_data["password2"])

        if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
            self.add_error('password2','las contraseñas no son iguales')

    # def clean_password1(self):
    #     if len(self.cleaned_data["password1"]) < 5:
    #         self.add_error('password1','la contaseña es muy corta, debe tener al menos 5 caracteres')


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'username',
                'style': '{ margin: 10px }'
            }
        )
    )

    password = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'contraseña',
                'style': '{ margin: 10px }'
            }
        )
    )

    # función "clean" indica a django que esta es una de las primeras validaciones a realizar
    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if not authenticate(username=username, password=password):
            raise forms.ValidationError('Los datos del usuario no son correctos')
        
        return self.cleaned_data
    

class UpdatePasswordForm(forms.Form):

    password1 = forms.CharField(
        label='Contraseña Actual',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'contraseña actual',
                'style': '{ margin: 10px }'
            }
        )
    )

    password2 = forms.CharField(
        label='Contraseña Nueva',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'contraseña nueva',
                'style': '{ margin: 10px }'
            }
        )
    )


class VerificationForm(forms.Form):
    codregistro = forms.CharField(label='Codigo de Registro', required=True)

    def __init__(self, pk, *args, **kwargs):
        self.id_user = pk
        super(VerificationForm, self).__init__(*args, **kwargs)


    def clean_codregistro(self):
        codigo = self.cleaned_data['codregistro']

        if len(codigo) == 6:
            # verificamos si el codigo y el id del usuario son válidos
            activo = User.objects.cod_validation(
                self.id_user,
                codigo
            )

            if not activo:
                raise forms.ValidationError('el código es incorrecto')
        else:
            raise forms.ValidationError('el código es incorrecto')


