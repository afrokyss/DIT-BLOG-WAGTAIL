# Generated by Django 3.1.7 on 2021-03-09 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_auto_20210309_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articleblogpage',
            name='subtitle',
            field=models.CharField(blank=True, help_text='Subject of article in CAPITALS', max_length=100, null=True),
        ),
    ]