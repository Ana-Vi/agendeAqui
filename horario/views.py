from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from horario.models import Horarios
from sistema.models import Usuario


# Create your views here.
@login_required(login_url="/")
def horario(request):
    salao = Usuario.objects.filter(codigo_auth_user=request.user.id)
    horario = Horarios.objects.filter(id_usuario=request.user.id).order_by('id')
    data = {
        'nome_funcao': 'Meu Horário',
        'id_usuario_salao': salao,
        'horario': horario,
        'usuario': Usuario.objects.filter(codigo_auth_user=request.user.id)[0].nome
    }
    if salao == 0 or salao == '':
        data['Erro']='Erro! Salão não encontrado!'

    return render(request, 'horario/horario.html', data)

@login_required(login_url="/")
def update(request, pk):
    if request.method == "GET":
        data = {
            'nomefuncao': 'Horário Funcionamento',
            'db': Horarios.objects.get(pk=pk),
            'usuario': Usuario.objects.filter(codigo_auth_user=request.user.id)[0].nome
        }
        return render(request, 'horario/cadastrar.html', data)
    else:
        hora_inicial = request.POST.get('hora_inicial')
        hora_final = request.POST.get('hora_final')

        horario = Horarios.objects.get(pk=pk)
        horario.hora_inicial = hora_inicial
        horario.hora_final = hora_final
        horario.save()
        return redirect('horario')
