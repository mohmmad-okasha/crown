# Generated by Django 4.2.3 on 2023-08-20 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0020_flight_bookings'),
    ]

    operations = [
        migrations.AddField(
            model_name='roles',
            name='flight_bookings',
            field=models.IntegerField(default=0),
        ),
    ]
