# Generated by Django 3.2.17 on 2023-02-12 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='interests',
            field=models.ManyToManyField(to='categories.Genre'),
        ),
    ]
