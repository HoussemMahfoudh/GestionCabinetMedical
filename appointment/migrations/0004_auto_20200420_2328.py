# Generated by Django 2.2 on 2020-04-20 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0003_disponibilty_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='available',
            field=models.BooleanField(default=False),
        ),
    ]
