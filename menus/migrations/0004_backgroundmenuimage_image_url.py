# Generated by Django 3.1.7 on 2021-03-07 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0003_backgroundmenuimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='backgroundmenuimage',
            name='image_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
