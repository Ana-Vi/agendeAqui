from django.db import models

# Create your models here.


class Procedimentos(models.Model):
    nome = models.CharField(max_length=50)
    duracao = models.TimeField()
    valor = models.FloatField()
    id_usuario = models.CharField(max_length=6)
    id_procedimento = models.CharField(max_length=6, default="")
