# Generated by Django 4.1.1 on 2022-10-28 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='wishlist',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]