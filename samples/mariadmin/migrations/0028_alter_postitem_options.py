# Generated by Django 4.2.4 on 2023-09-07 22:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mariadmin', '0027_postitem_postlowerbody'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='postitem',
            options={'ordering': ('-postDate',)},
        ),
    ]
