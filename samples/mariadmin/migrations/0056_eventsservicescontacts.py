# Generated by Django 4.2.4 on 2023-09-21 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mariadmin', '0055_remove_contacts_formariahillgardens'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventsServicesContacts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contactType', models.TextField()),
                ('contactValue', models.TextField()),
            ],
        ),
    ]
