# Generated by Django 4.1.6 on 2023-07-09 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_chatmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='roles',
            name='backups',
            field=models.IntegerField(default=0),
        ),
    ]
