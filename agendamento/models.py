from django.db import models

# Create your models here.


class Agendamentos(models.Model):
    id_usuario_salao = models.CharField(max_length=6)
    id_usuario_cliente = models.CharField(max_length=6)
    hora_inicial = models.TimeField()
    hora_final = models.TimeField()
    data = models.DateField()
    valor_total = models.FloatField()
    duracao_total = models.TimeField()