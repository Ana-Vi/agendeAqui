from django.shortcuts import render

# Create your views here.
def login(request):
    data = {
        'nomefuncao': 'Sistema',
    }
    return render(request, 'sistema/login.html', data)
