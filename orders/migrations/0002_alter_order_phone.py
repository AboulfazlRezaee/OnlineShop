# Generated by Django 5.0 on 2024-02-05 14:36

import phonenumber_field.modelfields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Phone Number'),
        ),
    ]