# Generated by Django 3.2.17 on 2023-02-16 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_alter_eventgenre_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='name',
            field=models.CharField(default='Gallery', max_length=250),
        ),
    ]
