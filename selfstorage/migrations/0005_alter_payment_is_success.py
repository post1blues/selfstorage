# Generated by Django 3.2.9 on 2021-11-22 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('selfstorage', '0004_auto_20211122_0255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='is_success',
            field=models.BooleanField(default=False, verbose_name='статус оплаты'),
        ),
    ]
