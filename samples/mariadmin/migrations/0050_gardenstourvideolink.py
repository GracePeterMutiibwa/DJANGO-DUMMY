# Generated by Django 4.2.4 on 2023-09-19 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mariadmin', '0049_vendorpage_pageimagelogo'),
    ]

    operations = [
        migrations.CreateModel(
            name='gardensTourVideoLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('videoUrl', models.TextField()),
            ],
        ),
    ]
