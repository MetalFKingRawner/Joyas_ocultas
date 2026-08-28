from django import forms
from .models import Resena


class ResenaForm(forms.ModelForm):
    class Meta:
        model = Resena
        fields = ['calificacion', 'comentario']
        widgets = {
            'calificacion': forms.RadioSelect,
            'comentario': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Cuéntale a otros exploradores cómo te fue...'}),
        }