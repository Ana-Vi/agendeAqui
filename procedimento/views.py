from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from procedimento.models import Procedimentos


# Create your views here.

@login_required(login_url="/")
def procedimento(request):
    data = {
        'nomefuncao': 'Procedimento',
        'db': Procedimentos.objects.filter(id_usuario= request.user.id)
    }
    return render(request, 'procedimento/procedimento.html', data)

@login_required(login_url="/")
def cadastrar(request):
    if request.method == "GET":
        data = {
            'nomefuncao': "Novo procedimento",
        }
        return render(request, 'procedimento/cadastrar.html', data)
    else:
        nome = request.POST.get('nome')
        duracao = request.POST.get('duracao')
        valor = request.POST.get('valor')
        id_usuario = request.user.id

        procedimento = Procedimentos(nome=nome, duracao=duracao,
                                     valor=valor, id_usuario=id_usuario)
        procedimento.save()
        return redirect('procedimento')


@login_required(login_url="/")
def update(request,pk):
    if request.method =="GET":
        data = {
            'nomefuncao' : 'Atualizar procedimento',
            'procedimento': Procedimentos.objects.get(pk=pk)
        }
        return render(request,'procedimento/cadastrar.html', data)
    else:
        nome = request.POST.get('nome')
        duracao = request.POST.get('duracao')
        valor = request.POST.get('valor')

        procedimento = Procedimentos.objects.get(pk=pk)
        procedimento.nome = nome
        procedimento.duracao = duracao
        procedimento.valor = valor
        procedimento.save()
        return redirect('procedimento')

@login_required(login_url="/")
def delete(request, pk):
    db = Procedimentos.objects.get(pk=pk)
    db.delete()
    return redirect('procedimento')