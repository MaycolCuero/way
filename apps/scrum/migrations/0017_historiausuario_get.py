# Generated by Django 2.2.5 on 2020-02-06 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrum', '0016_auto_20200117_1653'),
    ]

    operations = [
        migrations.AddField(
            model_name='historiausuario',
            name='get',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
