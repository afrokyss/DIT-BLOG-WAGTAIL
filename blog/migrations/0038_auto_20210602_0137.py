# Generated by Django 3.0.13 on 2021-06-02 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0037_blogauthor_biographie'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogauthor',
            name='biographie',
            field=models.TextField(max_length=255, null=True),
        ),
    ]