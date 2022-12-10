from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from sistema.models import Usuario
from horario.models import Horarios
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.
def login(request):
    if request.method == "GET":
        return render(request, 'sistema/login.html')
    else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        user = authenticate(username=username, password=senha)
        if user:
            login_django(request, user)
            return redirect('horario')
        else:
            data = {
                'Erro': 'Erro! Usuário incorreto!'
            }
            return render(request, 'sistema/login.html', data)



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
        usuario = Usuario.objects.filter(email=email)
        if usuario:
            data = {
                'Erro': 'Erro! O e-mail: ' + email + ' está sendo usado por outro cadastro!'
            }
            return render(request, 'sistema/cadastro.html', data)
        else:
            user = User.objects.filter(email=email)
            if user:
                data = {
                    'Erro': 'Erro! O e-mail: ' + email + ' está sendo usado por outro cadastro!'
                }
                return render(request, 'sistema/cadastro.html', data)
            else:
                user = User.objects.create_user(email, email, senha)
                user.save()
                usuario = Usuario(nome=nome, email=email, senha=senha, cpf=cpf, telefone=telefone, codigo_auth_user=user.id)
                usuario.save()
                for aux in range(0,7):
                    horario = Horarios(dia_semana = aux, id_usuario = user.id)
                    horario.save()
                return redirect('login')

@login_required(login_url="/")
def update(request):
    user = User.objects.get(pk=request.user.id)
    usuario = Usuario.objects.filter(codigo_auth_user=request.user.id)
    usuario = Usuario.objects.get(pk = usuario[0].id)
    if request.method == "GET":
        data = {
            'user' : user,
            'usuario': usuario,
        }
        return render(request, 'sistema/atualiza-user.html', data)
    else:
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')
        cpf = request.POST.get('cpf')
        telefone = request.POST.get('telefone')

        user.set_password(senha)
        user.save()
        usuario.nome = nome
        usuario.cpf = cpf
        usuario.telefone = telefone
        usuario.senha = senha
        usuario.save()
        return redirect('horario')

def erro404(request, exception):
    return render(request, '404.html')

def erro500(request, exception):
    return render(request,'500.html')