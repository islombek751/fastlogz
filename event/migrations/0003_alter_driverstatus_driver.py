# Generated by Django 3.2.9 on 2022-03-09 06:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eld', '0001_initial'),
        ('event', '0002_auto_20220307_1430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driverstatus',
            name='driver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='driver_status', to='eld.drivers'),
        ),
    ]
