# Generated by Django 4.2.3 on 2023-07-31 04:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Accounts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('debit', models.FloatField(max_length=10, null=True)),
                ('credit', models.FloatField(max_length=10, null=True)),
                ('user', models.CharField(max_length=50, null=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Airlines',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Airports',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_en', models.CharField(max_length=200)),
                ('name_ar', models.CharField(max_length=200)),
                ('code', models.SlugField(max_length=200, unique=True)),
                ('city', models.CharField(max_length=200)),
                ('status', models.IntegerField(choices=[(0, 'Disabled'), (1, 'Enabled')], default=1)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Bookings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_date', models.DateTimeField(max_length=50)),
                ('persons_number', models.IntegerField()),
                ('persons_names', models.CharField(max_length=200)),
                ('kids_number', models.IntegerField(default=0)),
                ('kids_names', models.CharField(blank=True, max_length=200)),
                ('kids_ages', models.CharField(blank=True, max_length=200)),
                ('hotel', models.CharField(max_length=50)),
                ('dates', models.CharField(max_length=100)),
                ('out_date', models.CharField(blank=True, max_length=100)),
                ('room_id', models.CharField(max_length=50)),
                ('room_type', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=50)),
                ('notes', models.CharField(blank=True, max_length=100)),
                ('user', models.CharField(blank=True, max_length=50)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Dashboard_buttons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('url', models.CharField(max_length=50)),
                ('icon', models.CharField(max_length=50)),
                ('color', models.CharField(max_length=50)),
                ('show', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Flight_dates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flight_id', models.IntegerField()),
                ('departure_date', models.DateTimeField(max_length=50)),
                ('arrival_date', models.DateTimeField(max_length=50)),
            ],
            options={
                'ordering': ['flight_id'],
            },
        ),
        migrations.CreateModel(
            name='Flights',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('airline', models.CharField(max_length=50)),
                ('from_airport', models.CharField(max_length=50)),
                ('to_airport', models.CharField(max_length=50)),
                ('departure_date', models.DateTimeField(max_length=50)),
                ('arrival_date', models.DateTimeField(max_length=50)),
                ('seats', models.IntegerField()),
                ('status', models.CharField(max_length=100)),
                ('notes', models.CharField(blank=True, max_length=100)),
                ('user', models.CharField(blank=True, max_length=50)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Hotels',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('area', models.CharField(blank=True, max_length=50)),
                ('rate', models.CharField(max_length=50)),
                ('allotment', models.IntegerField()),
                ('notes', models.CharField(blank=True, max_length=100)),
                ('user', models.CharField(blank=True, max_length=50)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log', models.CharField(max_length=500)),
                ('user_name', models.CharField(max_length=50)),
                ('time', models.DateTimeField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dark_mode', models.BooleanField()),
                ('lang', models.CharField(max_length=50)),
                ('primary_color', models.CharField(max_length=50)),
                ('back_color', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Rooms',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('room_id', models.CharField(max_length=50)),
                ('room_categ', models.CharField(blank=True, max_length=50)),
                ('room_type', models.CharField(max_length=50)),
                ('meals', models.CharField(blank=True, max_length=50)),
                ('persons', models.IntegerField()),
                ('range', models.CharField(max_length=1000)),
                ('notes', models.CharField(blank=True, max_length=100)),
                ('user', models.CharField(blank=True, max_length=50)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.hotels')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Room_dates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=50)),
                ('room_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.rooms')),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('users', models.IntegerField(default=0)),
                ('bookings', models.IntegerField(default=0)),
                ('hotels', models.IntegerField(default=0)),
                ('available_hotel', models.IntegerField(default=0)),
                ('hotels_report', models.IntegerField(default=0)),
                ('backups', models.IntegerField(default=0)),
                ('logs', models.IntegerField(default=0)),
                ('flights', models.IntegerField(default=0)),
                ('user_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
