# Generated by Django 4.1.5 on 2023-05-21 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0038_alter_room_dates_room_id_alter_rooms_room_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room_dates',
            name='room_id',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='rooms',
            name='room_id',
            field=models.CharField(max_length=50),
        ),
    ]
