# Generated by Django 4.2.3 on 2023-08-20 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0019_alter_flights_airline_alter_flights_from_airport_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Flight_bookings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('depart_date', models.DateTimeField(max_length=50)),
                ('type', models.CharField(max_length=50)),
                ('seats', models.IntegerField()),
                ('flight_code', models.CharField(max_length=50)),
                ('notes', models.CharField(blank=True, max_length=100)),
                ('user', models.CharField(blank=True, max_length=50)),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
