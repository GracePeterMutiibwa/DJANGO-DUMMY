# Generated by Django 4.2.4 on 2023-08-29 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mariadmin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageAsset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imageName', models.TextField()),
                ('imageSize', models.TextField()),
                ('imageData', models.ImageField(upload_to='assets/')),
            ],
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['modelName']},
        ),
    ]
