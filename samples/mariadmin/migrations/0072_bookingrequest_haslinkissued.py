# Generated by Django 4.2.4 on 2023-12-17 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mariadmin', '0071_alter_bookingtransaction_satisfieddate'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingrequest',
            name='hasLinkIssued',
            field=models.BooleanField(default=False),
        ),
    ]
