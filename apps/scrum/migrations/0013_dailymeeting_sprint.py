# Generated by Django 2.2.4 on 2019-11-17 05:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scrum', '0012_dailymeeting'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailymeeting',
            name='sprint',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='scrum.Sprint'),
        ),
    ]
