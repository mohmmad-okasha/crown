# Generated by Django 4.2.3 on 2023-07-17 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0009_logs'),
    ]

    operations = [
        migrations.AddField(
            model_name='roles',
            name='logs',
            field=models.IntegerField(default=0),
        ),
    ]