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
        return render(request, 'agendamento/cadastrar.html', data)
    else:
        hora_inicial = request.POST.get('hora_inicial')
        hora_final = request.POST.get('hora_final')
        data = request.POST.get('data')
        valor_total = request.POST.get('valor_total')
        duracao_total = request.POST.get('duracao_total')
        cliente = request.POST.get('cliente')

        agendamento = Agendamentos.objects.filter(id_usuario_salao= request.user.id, data = data, hora_inicial=hora_inicial, hora_final = hora_final)

        if agendamento:
            return HttpResponse('Erro! O horário: ' + data + '->' + hora_inicial + ' está sendo usado por outro cadastro')
        elif data == '':
            return HttpResponse('Insira a data')
        else:
            agendamento = Agendamentos(id_usuario_salao= request.user.id,hora_inicial=hora_inicial, hora_final=hora_final, data = data, valor_total=valor_total, duracao_total=duracao_total, cliente= cliente)
            agendamento.save()
            return redirect('agenda')


@login_required(login_url="/")
def agenda(request):
    salao = Usuario.objects.filter(codigo_auth_user = request.user.id)
    agenda = Agendamentos.objects.filter(id_usuario_salao = request.user.id)
    if salao == 0 or salao == '':
        return HttpResponse('Salão não encontrado')
    data = {
        'nome_funcao': 'Minha agenda',
        'id_usuario_salao': salao,
        'agenda': agenda,
    }
    return render(request, 'agendamento/agenda.html', data)

@login_required(login_url="/")
def update(request, pk):
    if request.method == "GET":
        data = {
            'db': Agendamentos.objects.get(pk=pk),
        }
        return render(request, "agendamento/cadastrar.html", data)
    else:
        data = {
            'db' : Agendamentos.objects.get(pk=pk),
        }

        hora_inicial = request.POST.get('hora_inicial')
        hora_final = request.POST.get('hora_final')
        data = request.POST.get('data')
        valor_total = request.POST.get('valor_total')
        duracao_total = request.POST.get('duracao_total')
        cliente = request.POST.get('cliente')

        agendamento = Agendamentos.objects.filter(id_usuario_salao=request.user.id, data=data,
                                                  hora_inicial=hora_inicial, hora_final=hora_final)

        if agendamento:
            return HttpResponse(
                'Erro! O horário: ' + data + '->' + hora_inicial + ' está sendo usado por outro cadastro')
        elif data == '':
            return HttpResponse('Insira a data')
        else:
            agendamento = Agendamentos.objects.get(id=pk)
            agendamento.hora_inicial = hora_inicial
            agendamento.hora_final = hora_final
            agendamento.data = data
            agendamento.valor_total = valor_total
            agendamento.duracao_total = duracao_total
            agendamento.cliente = cliente

            agendamento.save()
            return redirect('agenda')

