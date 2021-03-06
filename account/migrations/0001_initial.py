# Generated by Django 2.2 on 2020-04-18 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('date_of_birth', models.DateField()),
                ('phone_number', models.DecimalField(decimal_places=0, max_digits=8)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=128)),
                ('city', models.CharField(choices=[('T', 'Tunis'), ('N', 'Nabeul'), ('A', 'Ariana')], max_length=128)),
                ('address', models.CharField(max_length=255)),
                ('specialite', models.CharField(max_length=233, null=True)),
                ('picture', models.ImageField(default='user.png', max_length=1000, upload_to='')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_doctor', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
