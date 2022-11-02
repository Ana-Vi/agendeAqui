from django.http import HttpResponse
from django.shortcuts import render, redirect
from sistema.forms import UsuarioForm
from django.contrib.auth.models import User
from sistema.models import Usuario
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.
def login(request):
    if request.method == "GET":
        data = {
            'nomefuncao': 'Login',
        }
        return render(request, 'sistema/login.html')
    else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        user = authenticate(username=username, password=senha)
        if user:
            login_django(request, user)
            return redirect('home')
        else:
            return HttpResponse("Inválido")



def cadastro(request):
    if request.method == "GET":
        data = {
            'nomefuncao': 'Cadastrar Usuário',
        }
        return render(request, 'sistema/cadastro.html', data)
    else:
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        cpf = request.POST.get('cpf')
        telefone = request.POST.get('telefone')
        salao = request.POST.get('salao')
        if salao == 'on':
            salao = True
        else:
            salao = False
        url = request.POST.get('url')
        usuario = Usuario.objects.filter(email=email)
        if usuario:
            return HttpResponse('Erro! O e-mail: ' + email + ' está sendo usado por outro cadastro')
        else:
            user = User.objects.filter(email=email)
            if user:
                return HttpResponse('Erro! O e-mail: ' + email + ' está sendo usado por outro cadastro')
            else:
                user = User.objects.create_user(nome, email, senha)
                user.save()
                usuario = Usuario(nome=nome, email=email, senha=senha, cpf=cpf, telefone=telefone, salao=salao, url=url)
                usuario.save()
                return redirect('login')


@login_required(login_url="/")
def home(request):
    return render(request, 'sistema/home.html')
