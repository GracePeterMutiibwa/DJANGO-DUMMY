# Generated by Django 4.2.4 on 2023-12-17 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mariadmin', '0069_alter_bookingtransaction_detailsoftransaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingtransaction',
            name='issuedDate',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
