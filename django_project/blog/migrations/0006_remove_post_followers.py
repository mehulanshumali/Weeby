# Generated by Django 3.0.8 on 2020-07-25 02:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20200725_0200'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='followers',
        ),
    ]
