# Generated by Django 4.1.5 on 2023-02-02 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_test_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test_model',
            name='a',
            field=models.CharField(max_length=1),
        ),
    ]
