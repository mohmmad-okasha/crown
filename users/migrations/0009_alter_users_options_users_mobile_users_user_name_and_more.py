# Generated by Django 4.1.5 on 2023-02-04 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_remove_users_author'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='users',
            options={'ordering': ['id']},
        ),
        migrations.AddField(
            model_name='users',
            name='mobile',
            field=models.CharField(default='0', max_length=15),
        ),
        migrations.AddField(
            model_name='users',
            name='user_name',
            field=models.CharField(default='null', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='users',
            name='name',
            field=models.CharField(max_length=25),
        ),
    ]
