# Generated by Django 3.2.9 on 2021-12-17 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_projects'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projects',
            name='id',
        ),
        migrations.AddField(
            model_name='projects',
            name='ids',
            field=models.IntegerField(default=10, help_text='项目主键', primary_key=True, serialize=False, verbose_name='项目主键'),
            preserve_default=False,
        ),
    ]
