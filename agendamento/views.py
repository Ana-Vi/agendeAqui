from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from agendamento.models import Agendamentos
from horario.models import Horarios
from procedimento.models import Procedimentos
from sistema.models import Usuario
from datetime import datetime, timedelta


# Create your views here.


@login_required(login_url="/")
def cadastrar(request):
    if request.method == "GET":
        data = {
            'nomefuncao': 'Agendar Horário',
            'procedimentos': Procedimentos.objects.filter(id_usuario = request.user.id),
            'modo': 'create',
            'usuario': Usuario.objects.filter(codigo_auth_user=request.user.id)[0].nome

        }
        return render(request, 'agendamento/cadastrar.html', data)
    else:
        procedimento = Procedimentos.objects.get(pk=request.POST.get('procedimento'))
        hora_inicial = datetime.strptime(request.POST.get('hora_inicial'), '%H:%M').strftime('%H:%M')
        horas,minutos = map(int, hora_inicial.split(':'))
        timea_h_i = timedelta(hours=horas, minutes=minutos)
        duracao = procedimento.duracao.strftime('%H:%M')
        data = datetime.strptime(request.POST.get('data'), '%Y-%m-%d')
        cliente = request.POST.get('cliente')
        data_semana = data.weekday()
        horario = Horarios.objects.filter(id_usuario=request.user.id, dia_semana=data_semana)
        horah_inicial = horario[0].hora_final.strftime('%H:%M')
        horas, minutos = map(int, horah_inicial.split(':'))
        timeh_h_f = timedelta(hours=horas, minutes=minutos)
        horah_final = horario[0].hora_inicial.strftime('%H:%M')
        horas, minutos = map(int, horah_final.split(':'))
        timeh_h_i = timedelta(hours=horas, minutes=minutos)
        valor_total = procedimento.valor
        horas, minutos = map(int, duracao.split(':'))
        soma_duracao_total = timedelta(hours=horas, minutes=minutos)
        soma_hora_inicial = datetime.strptime(hora_inicial, '%H:%M')
        horaa_final = soma_hora_inicial + soma_duracao_total
        horaa_final = horaa_final.strftime('%H:%M')
        horas, minutos = map(int, horaa_final.split(':'))
        timea_h_f = timedelta(hours=horas, minutes=minutos)

        agendamento = Agendamentos.objects.filter(id_usuario_salao=request.user.id,
                                                  data=data,
                                                  hora_final__range=[hora_inicial, horaa_final]) \
                      | Agendamentos.objects.filter(id_usuario_salao=request.user.id,
                                                    data=data,
                                                    hora_inicial__range=[hora_inicial, horaa_final])

        if timea_h_i > timeh_h_f:
            context = {
                'Erro': 'Erro! O horário está após a hora de fechamento do salão',
                'create': 1,
                'update': 0,
                'usuario': Usuario.objects.filter(codigo_auth_user=request.user.id)[0].nome
            }
            return render(request, 'agendamento/cadastrar.html', context)
        if timea_h_f < timeh_h_i:
            context = {
                'Erro': 'Erro! O horário está antes da hora de abertura do salão',
                'create': 1,
                'update': 0,
                'usuario': Usuario.objects.filter(codigo_auth_user=request.user.id)[0].nome
            }
            return render(request, 'agendamento/cadastrar.html', context)
        if agendamento:
            context = {
                'Erro': 'Erro! O horário está sendo usado por outro cadastro!',
                'create': 1,
                'update': 0,
                'usuario': Usuario.objects.filter(codigo_auth_user=request.user.id)[0].nome
            }
            return render(request, 'agendamento/cadastrar.html', context)
        elif data == '':
            context = {
                'Erro': 'Insira a data',
                'create': 1,
                'update': 0,
                'usuario': Usuario.objects.filter(codigo_auth_user=request.user.id)[0].nome
            }
            return render(request, 'agendamento/cadastrar.html', context)
        else:
            agendamento_salvar = Agendamentos(id_usuario_salao= request.user.id,hora_inicial=hora_inicial, hora_final=horaa_final,
                                       data = data, valor_total=valor_total, duracao_total=procedimento.duracao, cliente= cliente,
                                       id_procedimento = procedimento.id)
            agendamento_salvar.save()
            return redirect('agenda')


@login_required(login_url="/")
def agenda(request):
    salao = Usuario.objects.filter(codigo_auth_user = request.user.id)
    dia = datetime.today()
    agenda = Agendamentos.objects.filter(id_usuario_salao = request.user.id, data = dia).extra(select={'procedimento': 'SELECT nome from procedimento_procedimentos WHERE id = agendamento_agendamentos.id_procedimento '})

    if salao == 0 or salao == '':
        context = {
            'Erro': 'Salão não encontrado!',
            'usuario': Usuario.objects.filter(codigo_auth_user=request.user.id)[0].nome
        }
        return render(request, 'agendamento/agenda.html',context)
    data = {
        'nome_funcao': 'Minha agenda',
        'id_usuario_salao': salao,
        'agenda': agenda,
        'usuario': Usuario.objects.filter(codigo_auth_user=request.user.id)[0].nome
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
            'modo': 'update',
            'usuario': Usuario.objects.filter(codigo_auth_user=request.user.id)[0].nome
        }
        data['db'].data = data['db'].data.strftime('%Y-%m-%d')
        return render(request, "agendamento/cadastrar.html", data)
    else:
        hora_inicial = datetime.strptime(request.POST.get('hora_inicial'), '%H:%M').strftime('%H:%M')
        horas, minutos = map(int, hora_inicial.split(':'))
        timea_h_i = timedelta(hours=horas, minutes=minutos)
        duracao = procedimento.duracao.strftime('%H:%M')
        data = datetime.strptime(request.POST.get('data'), '%Y-%m-%d')
        cliente = request.POST.get('cliente')
        data_semana = data.weekday()
        horario = Horarios.objects.filter(id_usuario=request.user.id, dia_semana=data_semana)
        horah_inicial = horario[0].hora_final.strftime('%H:%M')
        horas, minutos = map(int, horah_inicial.split(':'))
        timeh_h_f = timedelta(hours=horas, minutes=minutos)
        horah_final = horario[0].hora_inicial.strftime('%H:%M')
        horas, minutos = map(int, horah_final.split(':'))
        timeh_h_i = timedelta(hours=horas, minutes=minutos)
        valor_total = procedimento.valor
        horas, minutos = map(int, duracao.split(':'))
        soma_duracao_total = timedelta(hours=horas, minutes=minutos)
        soma_hora_inicial = datetime.strptime(hora_inicial, '%H:%M')
        horaa_final = soma_hora_inicial + soma_duracao_total
        horaa_final = horaa_final.strftime('%H:%M')
        horas, minutos = map(int, horaa_final.split(':'))
        timea_h_f = timedelta(hours=horas, minutes=minutos)

        agendamento = Agendamentos.objects.filter(id_usuario_salao=request.user.id,
                                                  data=data,
                                                  hora_final__range=[hora_inicial, horaa_final])\
                      |Agendamentos.objects.filter(id_usuario_salao=request.user.id,
                                                   data=data,
                                                   hora_inicial__range=[hora_inicial, horaa_final])

        for aux in agendamento:
            if aux and aux.id !=pk:
                context = {
                    'Erro': 'Erro! O horário está sendo usado por outro cadastro!',
                    'create':0,
                    'update':1,
                    'id': pk,
                    'usuario': Usuario.objects.filter(codigo_auth_user=request.user.id)[0].nome
                }
                return render(request, 'agendamento/cadastrar.html', context)

        if timea_h_i > timeh_h_f:
            context = {
                'Erro': 'Erro! O horário está após a hora de fechamento do salão',
                'create': 0,
                'update': 1,
                'id': pk,
                'usuario': Usuario.objects.filter(codigo_auth_user=request.user.id)[0].nome
            }
            return render(request, 'agendamento/cadastrar.html', context)
        elif timea_h_f < timeh_h_i:
            context = {
                'Erro': 'Erro! O horário está antes da hora de abertura do salão',
                'create': 0,
                'update': 1,
                'id': pk,
                'usuario': Usuario.objects.filter(codigo_auth_user=request.user.id)[0].nome
            }
            return render(request, 'agendamento/cadastrar.html', context)
        elif data == '':
            context = {
                'Erro': 'Insira a data',
                'create': 0,
                'update': 1,
                'id': pk,
                'usuario': Usuario.objects.filter(codigo_auth_user=request.user.id)[0].nome
            }
            return render(request, 'agendamento/cadastrar.html', context)
        else:
            agendamento_salvar = Agendamentos.objects.get(id=pk)
            agendamento_salvar.hora_inicial = hora_inicial
            agendamento_salvar.hora_final = horaa_final
            agendamento_salvar.data = data
            agendamento_salvar.valor_total = valor_total
            agendamento_salvar.duracao_total = procedimento.duracao
            agendamento_salvar.cliente = cliente
            agendamento_salvar.id_usuario_salao = request.user.id

            agendamento_salvar.save()
            return redirect('agenda')


@login_required(login_url="/")
def delete(request, pk):
    db = Agendamentos.objects.get(pk=pk)
    db.delete()
    return redirect('agenda')

