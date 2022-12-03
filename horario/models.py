from django.db import models

# Create your models here.


class Horarios(models.Model):
    hora_inicial: models.TimeField(default='')
    hora_final: models.TimeField(default='')
    dia_semana: models.IntegerField()
    id_usuario: models.CharField()