# Generated by Django 4.2.7 on 2023-11-09 16:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='todo',
            options={'ordering': ('title',)},
        ),
    ]
