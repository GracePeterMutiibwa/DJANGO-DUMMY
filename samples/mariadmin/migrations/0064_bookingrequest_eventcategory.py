# Generated by Django 4.2.4 on 2023-12-14 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mariadmin', '0063_alter_bookingrequest_venueusagedate'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingrequest',
            name='eventCategory',
            field=models.TextField(default=''),
        ),
    ]
