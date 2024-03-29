# Generated by Django 4.1.7 on 2023-06-17 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('base', '0008_customer_last_login'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this customer belongs to.', related_name='customer_set', related_query_name='customer', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='customer',
            name='is_superuser',
            field=models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status'),
        ),
        migrations.AddField(
            model_name='customer',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this customer.', related_name='customer_set', related_query_name='customer', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
