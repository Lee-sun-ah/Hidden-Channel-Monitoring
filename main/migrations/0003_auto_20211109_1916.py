# Generated by Django 3.2.8 on 2021-11-09 10:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20211029_2201'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TelChannel',
        ),
        migrations.DeleteModel(
            name='TelChat',
        ),
    ]
