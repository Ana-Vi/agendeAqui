from django.shortcuts import render

# Create your views here.
def home(request):
    data = {
        'nomefuncao': 'Horário',
    }
    return render(request, 'horario.html', data)
