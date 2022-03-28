# Generated by Django 3.2.9 on 2022-03-07 14:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eld', '0001_initial'),
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='livedata',
            name='country',
            field=models.CharField(blank=True, editable=False, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='livedata',
            name='truck',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='eld.vehicle'),
        ),
    ]
