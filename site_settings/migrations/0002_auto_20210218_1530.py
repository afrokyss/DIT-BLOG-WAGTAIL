# Generated by Django 3.1.6 on 2021-02-18 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_settings', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='socialmediasettings',
            name='youtube',
        ),
        migrations.AddField(
            model_name='socialmediasettings',
            name='instagram',
            field=models.URLField(blank=True, help_text='Instagram Channel URL', null=True),
        ),
    ]
