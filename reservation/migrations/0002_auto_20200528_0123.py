# Generated by Django 2.2 on 2020-05-28 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservationmateriel',
            name='available',
            field=models.BooleanField(null=True),
        ),
    ]
