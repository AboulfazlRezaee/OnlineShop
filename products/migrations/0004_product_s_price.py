# Generated by Django 5.0 on 2024-01-28 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_image_alter_comment_author_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='s_price',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
