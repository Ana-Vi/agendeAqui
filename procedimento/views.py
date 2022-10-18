from django.shortcuts import render

# Create your views here.
def home(request):
    data = {
        'nomefuncao': 'Procedimento',
    }
    return render(request, 'procedimento.html', data)
