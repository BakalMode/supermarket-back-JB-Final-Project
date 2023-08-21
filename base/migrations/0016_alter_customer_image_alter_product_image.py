# Generated by Django 4.1.7 on 2023-06-26 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_product_description_product_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
    ]
