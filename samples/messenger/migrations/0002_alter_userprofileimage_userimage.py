# Generated by Django 4.2.4 on 2023-08-19 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofileimage',
            name='userImage',
            field=models.ImageField(blank=True, null=True, upload_to='profile-images/'),
        ),
    ]
