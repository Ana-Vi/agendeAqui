from django.shortcuts import render, redirect
from sistema.forms import UsuarioForm
from sistema.models import Usuario

# Create your views here.
def login(request):
    data = {
        'nomefuncao': 'Login',
    }
    return render(request, 'sistema/login.html', data)

def entra(request, cpf):
    form = UsuarioForm(request.POST or None)
    if form.is_valid():
        if Usuario.objects.get(cpf=cpf):
            return redirect('home')
def registra(request):
    data = {
        'nomefuncao': 'Cadastrar Usuário',
        'form': UsuarioForm()
    }
    return render(request, 'sistema/registra.html', data)

def create(request):
    form = UsuarioForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('login')

def home(request):
    data = {}
    return render(request, 'sistema/home.html', data)
