# Generated by Django 4.2.3 on 2023-07-16 18:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_logs_remove_bookings_in_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='logs',
            old_name='log',
            new_name='logs',
        ),
    ]