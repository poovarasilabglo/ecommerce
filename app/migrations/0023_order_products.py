# Generated by Django 4.1.1 on 2022-10-30 04:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_order_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.products'),
        ),
    ]