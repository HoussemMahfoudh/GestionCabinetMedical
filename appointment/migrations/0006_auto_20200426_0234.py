# Generated by Django 2.2 on 2020-04-26 01:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0005_auto_20200426_0232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='event',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='appointment.Event'),
        ),
    ]
