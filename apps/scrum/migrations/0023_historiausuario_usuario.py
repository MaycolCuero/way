# Generated by Django 3.0.3 on 2020-04-11 15:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('scrum', '0022_auto_20200311_2348'),
    ]

    operations = [
        migrations.AddField(
            model_name='historiausuario',
            name='usuario',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
