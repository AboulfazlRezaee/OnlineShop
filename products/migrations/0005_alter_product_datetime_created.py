# Generated by Django 5.0 on 2024-01-30 08:43

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_product_s_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='datetime_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]