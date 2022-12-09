# Generated by Django 3.1.4 on 2022-12-09 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('horario', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='horarios',
            name='dia_semana',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='horarios',
            name='hora_final',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='horarios',
            name='hora_inicial',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='horarios',
            name='id_usuario',
            field=models.CharField(default='', max_length=6),
        ),
    ]
