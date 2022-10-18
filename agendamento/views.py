from django.shortcuts import render

# Create your views here.
def home(request):
    data = {
        'nomefuncao': 'Agendamento',
    }
    return render(request, 'agendamento.html', data)
