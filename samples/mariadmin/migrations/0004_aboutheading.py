# Generated by Django 4.2.4 on 2023-08-31 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mariadmin', '0003_imageasset_uploaddate'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutHeading',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headingName', models.TextField(max_length=250)),
            ],
        ),
    ]
