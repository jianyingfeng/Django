# Generated by Django 3.1.6 on 2022-01-12 07:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interfaces', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='interfaces',
            options={'ordering': ['id'], 'verbose_name': '接口表', 'verbose_name_plural': '接口表'},
        ),
    ]