from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from agendamento.models import Agendamentos
from horario.models import Horarios
from procedimento.models import Procedimentos
from sistema.models import Usuario
from datetime import datetime


# Create your views here.


@login_required(login_url="/")
def cadastrar(request):
    if request.method == "GET":
        data = {
            'nomefuncao': 'Agendar Horário',
            'procedimentos': Procedimentos.objects.filter(id_usuario = request.user.id),
            'modo': 'create'
        }
        return render(request, 'agendamento/cadastrar.html', data)
    else:
        hora_inicial = datetime.strptime(request.POST.get('hora_inicial'), '%H:%M').strftime('%H:%M')
        data = datetime.strptime(request.POST.get('data'), '%Y-%m-%d')
        cliente = request.POST.get('cliente')
        procedimento = Procedimentos.objects.get(pk = request.POST.get('procedimento'))
        valor_total = procedimento.valor
        duracao_total = procedimento.duracao
        data_semana = data.weekday()

        horario = Horarios.objects.filter(id_usuario=request.user.id, dia_semana = data_semana)
        hora_final = hora_inicial + procedimento.duracao.strftime('%H:%M')
        agendamento = Agendamentos.objects.filter(id_usuario_salao= request.user.id, data = data,
                                                  hora_inicial=hora_inicial, hora_final = hora_final)

        if horario[0].hora_final.strftime('%H:%M') < hora_final:
            context = {
                'Erro': 'Erro! O horário está após a hora de fechamento do salão'
            }
            return render(request, 'agendamento/cadastrar', context)
        if horario[0].hora_inicial.strftime('%H:%M') > hora_inicial:
            context = {
                'Erro': 'Erro! O horário está antes da hora de abertura do salão'
            }
            return render(request, 'agendamento/cadastrar', context)
        if agendamento:
            context = {
                'Erro': 'Erro! O horário está sendo usado por outro cadastro!'
            }
            return render(request, 'agendamento/cadastrar.html', context)
        elif data == '':
            context = {
                'Erro': 'Insira a data'
            }
            return render(request, 'agendamento/cadastrar.html', context)
        else:
            agendamento = Agendamentos(id_usuario_salao= request.user.id,hora_inicial=hora_inicial, hora_final=hora_final,
                                       data = data, valor_total=valor_total, duracao_total=duracao_total, cliente= cliente,
                                       id_procedimento = procedimento.id)
            agendamento.save()
            return redirect('agenda')


@login_required(login_url="/")
def agenda(request):
    salao = Usuario.objects.filter(codigo_auth_user = request.user.id)
    agenda = Agendamentos.objects.filter(id_usuario_salao = request.user.id)
    if salao == 0 or salao == '':
        context = {
            'Erro': 'Salão não encontrado!'
        }
        return render(request, 'agendamento/agenda.html',context)
    data = {
        'nome_funcao': 'Minha agenda',
        'id_usuario_salao': salao,
        'agenda': agenda,
    }
    return render(request, 'agendamento/agenda.html', data)

@login_required(login_url="/")
def update(request, pk):
    agendamento = Agendamentos.objects.get(pk=pk)
    procedimento = Procedimentos.objects.get(pk=agendamento.id_procedimento)
    if request.method == "GET":
        data = {
            'db': agendamento,
            'procedimento': procedimento,
            'modo': 'update'
        }
        data['db'].data = data['db'].data.strftime('%d/%m/%Y')
        return render(request, "agendamento/cadastrar.html", data)
    else:
        hora_inicial = datetime.strptime(request.POST.get('hora_inicial'), '%H:%M').strftime('%H:%M')
        data = datetime.strptime(request.POST.get('data'), '%Y-%m-%d')
        hora_final = hora_inicial + procedimento.duracao.strftime('%H:%M')
        cliente = request.POST.get('cliente')
        valor_total = procedimento.valor
        duracao_total = procedimento.duracao
        data_semana = data.weekday()
        agendamento = Agendamentos.objects.filter(id_usuario_salao=request.user.id, data=data,
                                                  hora_inicial=hora_inicial, hora_final=hora_final)
        horario = Horarios.objects.filter(id_usuario=request.user.id, dia_semana=data_semana)

        if horario[0].hora_final.strftime('%H:%M') < hora_final:
            context = {
                'Erro': 'Erro! O horário está após a hora de fechamento do salão'
            }
            return render(request, 'agendamento/cadastrar', context)
        if horario[0].hora_inicial.strftime('%H:%M') > hora_inicial:
            context = {
                'Erro': 'Erro! O horário está antes da hora de abertura do salão'
            }
            return render(request, 'agendamento/cadastrar', context)
        if agendamento:
            context = {
                'Erro': 'Erro! O horário está sendo usado por outro cadastro!'
            }
            return render(request, 'agendamento/cadastrar.html', context)
        elif data == '':
            context = {
                'Erro': 'Insira a data'
            }
            return render(request, 'agendamento/cadastrar.html', context)
        else:
            agendamento = Agendamentos.objects.get(id=pk)
            agendamento.hora_inicial = hora_inicial
            agendamento.hora_final = hora_final
            agendamento.data = data
            agendamento.valor_total = valor_total
            agendamento.duracao_total = duracao_total
            agendamento.cliente = cliente
            agendamento.id_usuario_salao = request.user.id

            agendamento.save()
            return redirect('agenda')


@login_required(login_url="/")
def delete(request, pk):
    db = Agendamentos.objects.get(pk=pk)
    db.delete()
    return redirect('agenda')

