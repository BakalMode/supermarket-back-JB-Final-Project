# Generated by Django 4.1.7 on 2023-06-24 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_alter_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='category_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
