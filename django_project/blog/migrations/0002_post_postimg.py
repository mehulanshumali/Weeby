# Generated by Django 3.0.5 on 2020-05-17 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='postimg',
            field=models.ImageField(null=True, upload_to='post'),
        ),
    ]
