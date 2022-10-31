from django.forms import ModelForm
from sistema.models import Usuario

class UsuarioForm(ModelForm):
    class Meta:
        model = Usuario
        fields = ['cpf', 'senha','nome', 'telefone', 'salao', 'url', 'email']