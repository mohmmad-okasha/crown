# Generated by Django 4.2.3 on 2023-08-22 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0024_rename_flight_code_flight_bookings_go_flight_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight_bookings',
            name='back_flight_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='flight_bookings',
            name='return_date',
            field=models.DateTimeField(blank=True, max_length=50, null=True),
        ),
    ]
