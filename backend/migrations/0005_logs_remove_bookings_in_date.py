# Generated by Django 4.2.3 on 2023-07-16 18:01

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_bookings_in_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log', models.CharField(max_length=50)),
                ('user_name', models.CharField(max_length=50)),
                ('time', models.DateTimeField(max_length=50)),
            ],
            managers=[
                ('second_db_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.RemoveField(
            model_name='bookings',
            name='in_date',
        ),
    ]