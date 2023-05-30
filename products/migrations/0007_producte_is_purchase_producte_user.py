# Generated by Django 4.1.7 on 2023-03-24 00:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0006_alter_producte_off'),
    ]

    operations = [
        migrations.AddField(
            model_name='producte',
            name='is_purchase',
            field=models.BooleanField(blank=True, null=True, verbose_name='purchase'),
        ),
        migrations.AddField(
            model_name='producte',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]