# Generated by Django 4.2.4 on 2023-09-19 09:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mariadmin', '0050_gardenstourvideolink'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='venueitem',
            name='venueImageUrl',
        ),
    ]
