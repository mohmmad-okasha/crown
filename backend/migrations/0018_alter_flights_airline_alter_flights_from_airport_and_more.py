# Generated by Django 4.2.3 on 2023-08-01 06:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0017_remove_airlines_name_airlines_city_airlines_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flights',
            name='airline',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.airlines'),
        ),
        migrations.AlterField(
            model_name='flights',
            name='from_airport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='From_Airport', to='backend.airports'),
        ),
        migrations.AlterField(
            model_name='flights',
            name='to_airport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='To_Airport', to='backend.airports'),
        ),
    ]
