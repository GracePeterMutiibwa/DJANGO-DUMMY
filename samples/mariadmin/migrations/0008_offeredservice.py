# Generated by Django 4.2.4 on 2023-09-02 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mariadmin', '0007_rightcard'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfferedService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serviceName', models.TextField()),
                ('serviceDetails', models.TextField()),
            ],
        ),
    ]
