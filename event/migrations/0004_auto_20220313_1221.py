# Generated by Django 3.2.9 on 2022-03-13 12:21

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0003_alter_driverstatus_driver'),
    ]

    operations = [
        migrations.AddField(
            model_name='driverstatus',
            name='note',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='driverstatus',
            name='point',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326),
        ),
    ]
