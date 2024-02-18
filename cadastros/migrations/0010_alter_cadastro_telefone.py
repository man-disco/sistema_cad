# Generated by Django 5.0.1 on 2024-02-18 22:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0009_telefone_alter_cadastro_telefone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cadastro',
            name='telefone',
            field=models.CharField(blank=True, max_length=11, null=True, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '(99) 99999-9999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
        ),
    ]