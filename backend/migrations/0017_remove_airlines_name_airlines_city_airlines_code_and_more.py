# Generated by Django 4.2.3 on 2023-08-01 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0016_remove_airports_name_airports_city_airports_code_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='airlines',
            name='name',
        ),
        migrations.AddField(
            model_name='airlines',
            name='city',
            field=models.CharField(default='', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='airlines',
            name='code',
            field=models.CharField(default='', max_length=200, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='airlines',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='airlines',
            name='name_ar',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='airlines',
            name='name_en',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='airlines',
            name='status',
            field=models.IntegerField(default=1, null=True),
        ),
        migrations.AddField(
            model_name='airlines',
            name='updated_on',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
