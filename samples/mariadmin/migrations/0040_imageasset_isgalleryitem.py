# Generated by Django 4.2.4 on 2023-09-15 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mariadmin', '0039_alter_vendorservice_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='imageasset',
            name='isGalleryItem',
            field=models.BooleanField(default=False),
        ),
    ]
