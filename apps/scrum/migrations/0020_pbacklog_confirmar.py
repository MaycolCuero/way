# Generated by Django 3.0.3 on 2020-02-23 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrum', '0019_sreview_id_pbacklog'),
    ]

    operations = [
        migrations.AddField(
            model_name='pbacklog',
            name='confirmar',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
