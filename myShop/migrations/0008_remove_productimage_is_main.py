# Generated by Django 4.0.5 on 2022-08-03 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myShop', '0007_alter_productimage_is_main'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productimage',
            name='is_main',
        ),
    ]
