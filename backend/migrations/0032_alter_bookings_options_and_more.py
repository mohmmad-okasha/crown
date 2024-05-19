# Generated by Django 4.2.6 on 2024-05-18 09:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0031_alter_bookings_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookings',
            options={'ordering': ['id']},
        ),
        migrations.RemoveIndex(
            model_name='bookings',
            name='backend_boo_status_b03f18_idx',
        ),
        migrations.RemoveIndex(
            model_name='bookings',
            name='backend_boo_hotel_301f64_idx',
        ),
        migrations.RemoveIndex(
            model_name='bookings',
            name='backend_boo_room_ty_314704_idx',
        ),
    ]
