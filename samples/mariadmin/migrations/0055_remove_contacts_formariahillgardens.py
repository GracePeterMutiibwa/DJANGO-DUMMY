# Generated by Django 4.2.4 on 2023-09-21 05:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mariadmin', '0054_contacts_formariahillgardens'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contacts',
            name='forMariaHillGardens',
        ),
    ]
