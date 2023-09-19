# Generated by Django 4.2.4 on 2023-09-14 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mariadmin', '0034_alter_pagecategory_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='VendorPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pageName', models.TextField()),
                ('pageDescription', models.TextField()),
                ('pageCategory', models.TextField()),
                ('isVisible', models.BooleanField(default=False)),
                ('dateAdded', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-dateAdded',),
            },
        ),
    ]
