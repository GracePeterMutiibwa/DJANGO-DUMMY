# Generated by Django 4.2.4 on 2023-09-14 19:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mariadmin', '0037_socialmediahandles'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendorservice',
            name='dateAdded',
            field=models.DateTimeField(auto_created=True, default=django.utils.timezone.now),
        ),
    ]
