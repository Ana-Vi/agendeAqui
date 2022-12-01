from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from agendamento.models import Agendamentos
from sistema.models import Usuario


# Create your views here.

@login_required(login_url="/")
def cadastrar(request):
    if request.method == "GET":
        data = {
            'nomefuncao': 'Agendar Horário',
        }
        return render(request, 'agendamento.html', data)
    else:
        id_usuario_salao = request.POST.get('salao')
        id_usuario_cliente = request.user.id
        hora_inicial = request.POST.get('hora_inicial')
        hora_final = request.POST.get('hora_final')
        data = request.POST.get('data')
        valor_total = request.POST.get('valor_total')
        duracao_total = request.POST.get('duracao_total')

        agendamento = Agendamentos.objects.filter(data = data, hora_inicial=hora_inicial, hora_final = hora_final)

        if agendamento:
            return HttpResponse('Erro! O horário: ' + data + '->' + hora_inicial + ' está sendo usado por outro cadastro')
        elif id_usuario_salao == '':
            return HttpResponse('Insira o salão')
        elif data == '':
            return HttpResponse('Insira a data')
        else:
            agendamento = Agendamentos(id_usuario_salao = id_usuario_salao, id_usuario_cliente = id_usuario_cliente, hora_inicial=hora_inicial, hora_final=hora_final, data = data, valor_total=valor_total, duracao_total=duracao_total)
            return redirect('home')


@login_required(login_url="/")
def agenda(request):
    if request.method == 'GET':
        salao = Usuario.objects.filter(codigo_auth_user = request.user.id)
        agenda = Agendamentos.objects.filter(id_usuario_salao = 1)
        if salao == 0 or salao == '':
            return HttpResponse('Salão não encontrado')
        data = {
            'nome_funcao': 'Minha agenda',
            'id_usuario_salao': salao,
            'agenda': agenda,
        }
        return render(request, 'agendamento/agenda.html', data)

