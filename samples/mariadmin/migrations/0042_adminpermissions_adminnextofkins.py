# Generated by Django 4.2.4 on 2023-09-18 01:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mariadmin', '0041_emailreset'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminPermissions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('websiteEditor', models.BooleanField(default=False)),
                ('blogEditor', models.BooleanField(default=False)),
                ('thirdPartyEditor', models.BooleanField(default=False)),
                ('commUtilities', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='AdminNextOfKins',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addedDate', models.DateTimeField(auto_now_add=True)),
                ('adminUserName', models.TextField()),
                ('adminEmailAddress', models.TextField()),
                ('associatedPermissions', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_permissions', to='mariadmin.adminpermissions')),
            ],
            options={
                'ordering': ('-addedDate',),
            },
        ),
    ]
