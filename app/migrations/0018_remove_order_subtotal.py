# Generated by Django 4.1.1 on 2022-10-26 10:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_cart_is_active_order_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='subtotal',
        ),
    ]