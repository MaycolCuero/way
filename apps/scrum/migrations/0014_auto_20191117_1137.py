# Generated by Django 2.2.4 on 2019-11-17 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrum', '0013_dailymeeting_sprint'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sreview',
            old_name='descripcion',
            new_name='observaciones',
        ),
        migrations.RenameField(
            model_name='sreview',
            old_name='id_sprint',
            new_name='sprint',
        ),
        migrations.AddField(
            model_name='sreview',
            name='logros',
            field=models.CharField(blank=True, max_length=600, null=True),
        ),
    ]
