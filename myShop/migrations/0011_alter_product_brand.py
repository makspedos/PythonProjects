# Generated by Django 4.0.5 on 2023-05-25 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myShop', '0010_brand'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
