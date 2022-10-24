from django.shortcuts import render, redirect
from sistema.forms import UsuarioForm
from sistema.models import Usuario

# Create your views here.
def login(request):
    data = {
        'nomefuncao': 'Login',
    }
    return render(request, 'sistema/login.html', data)

def cadastro(request):
    return render(request, 'sistema/cadastro.html')