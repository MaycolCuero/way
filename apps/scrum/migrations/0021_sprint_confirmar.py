# Generated by Django 3.0.3 on 2020-03-05 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrum', '0020_pbacklog_confirmar'),
    ]

    operations = [
        migrations.AddField(
            model_name='sprint',
            name='confirmar',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
