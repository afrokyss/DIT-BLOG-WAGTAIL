# Generated by Django 3.1.7 on 2021-02-23 19:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_blogdetailpage_article_summary'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogdetailpage',
            old_name='article_summary',
            new_name='chapo',
        ),
    ]