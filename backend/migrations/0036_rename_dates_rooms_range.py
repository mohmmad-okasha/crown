# Generated by Django 4.1.5 on 2023-05-21 08:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0035_dashboard_buttons_show'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rooms',
            old_name='dates',
            new_name='range',
        ),
    ]