# Generated by Django 2.2.4 on 2019-10-23 05:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('proyecto', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoriaUsuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('como_usuario', models.CharField(max_length=300)),
                ('quiero', models.TextField()),
                ('para', models.TextField()),
                ('estado', models.BooleanField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Scrum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proyecto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proyecto.Proyecto')),
            ],
        ),
        migrations.CreateModel(
            name='Sbacklog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField()),
                ('n_horas', models.IntegerField()),
                ('estado', models.BooleanField(blank=True, null=True)),
                ('get', models.BooleanField(blank=True, null=True)),
                ('id_historia', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='scrum.HistoriaUsuario')),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pbacklog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=300)),
                ('id_scrum', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='scrum.Scrum')),
            ],
        ),
        migrations.AddField(
            model_name='historiausuario',
            name='id_pbacklog',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='scrum.Pbacklog'),
        ),
    ]
