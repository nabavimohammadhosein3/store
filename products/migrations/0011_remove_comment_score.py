# Generated by Django 4.1.7 on 2023-03-30 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_remove_producte_exist_storeroom_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='score',
        ),
    ]
