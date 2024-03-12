# Generated by Django 3.2.4 on 2022-04-13 06:35

import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('phone_number', models.CharField(blank=True, max_length=14, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Enter a valid phone number.', regex='^((251)|(\\+251)|(00251)|(0)|)[7-9][0-9]{8}$')])),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('role', models.CharField(choices=[('super admin', 'super admin'), ('admin', 'admin'), ('staff', 'staff'), ('guest', 'guest')], max_length=200)),
                ('is_active', models.BooleanField(default=True)),
                ('register_date', models.DateField(default=django.utils.timezone.now)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
