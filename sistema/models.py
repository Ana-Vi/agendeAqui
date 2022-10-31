from django.db import models

# Create your models here.
class Usuario(models.Model):
    cpf = models.CharField(max_length=15)
    senha = models.CharField(max_length=500)
    nome = models.CharField(max_length=255)
    telefone = models.CharField(max_length=15)
    salao = models.BooleanField()
    url = models.TextField(default='')
    email = models.CharField(max_length=100, default='')