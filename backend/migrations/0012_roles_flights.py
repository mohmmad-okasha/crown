# Generated by Django 4.2.3 on 2023-07-26 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0011_alter_logs_log'),
    ]

    operations = [
        migrations.AddField(
            model_name='roles',
            name='flights',
            field=models.IntegerField(default=0),
        ),
    ]
