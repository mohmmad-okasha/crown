# Generated by Django 4.2.3 on 2023-07-16 20:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_rename_logs_logs_log'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Logs',
        ),
    ]
