from django.db import models

# Create your models here.


class Horarios(models.Model):
    hora_inicial = models.TimeField(null=True)
    hora_final = models.TimeField(null=True)
    dia_semana = models.IntegerField(default=0)
    id_usuario = models.CharField(max_length=6, default="")