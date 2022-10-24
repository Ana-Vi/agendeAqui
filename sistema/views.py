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
    data = {}
    data['form'] = UsuarioForm()
    return render(request, 'sistema/cadastro.html', data)

def create(request):
    form = UsuarioForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('home')

def home(request):
    return render(request, 'sistema/home.html')

