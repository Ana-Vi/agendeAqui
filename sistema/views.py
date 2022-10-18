from django.shortcuts import render

# Create your views here.
def home(request):
    data = {
        'nomefuncao': 'Sistema',
    }
    return render(request, 'sistema.html', data)
