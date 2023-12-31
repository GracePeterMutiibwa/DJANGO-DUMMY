# Generated by Django 4.2.4 on 2023-09-14 16:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mariadmin', '0036_vendorpage_vendordistrict_vendorservice_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialMediaHandles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facebookHandle', models.TextField(blank=True, null=True)),
                ('twitterHandle', models.TextField(blank=True, null=True)),
                ('instagramHandle', models.TextField(blank=True, null=True)),
                ('whatsappHandle', models.TextField(blank=True, null=True)),
                ('associatedVendorPage', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='vendor_handles', to='mariadmin.vendorpage')),
            ],
        ),
    ]
