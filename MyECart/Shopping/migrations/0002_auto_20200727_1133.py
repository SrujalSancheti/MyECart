# Generated by Django 3.0.8 on 2020-07-27 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shopping', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='', upload_to='Shopping/images'),
        ),
    ]
