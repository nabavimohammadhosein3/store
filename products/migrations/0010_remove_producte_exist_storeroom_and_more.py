# Generated by Django 4.1.7 on 2023-03-28 18:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_alter_comment_score'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producte',
            name='exist_storeroom',
        ),
        migrations.RemoveField(
            model_name='producte',
            name='pr_numbers',
        ),
    ]
