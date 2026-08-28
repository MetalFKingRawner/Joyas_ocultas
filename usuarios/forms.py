from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    nombre_explorador = forms.CharField(max_length=50, required=False, label="Nombre de explorador")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            user.perfilusuario.nombre_explorador = self.cleaned_data.get('nombre_explorador', '')
            user.perfilusuario.save()
        return user