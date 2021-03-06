# Generated by Django 3.0.13 on 2021-07-05 01:09

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0060_fix_workflow_unique_constraint'),
        ('blog', '0040_auto_20210609_2134'),
    ]

    operations = [
        migrations.CreateModel(
            name='Navbar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('menu_items', wagtail.core.fields.StreamField([('external_link', wagtail.core.blocks.StructBlock([('display_text', wagtail.core.blocks.CharBlock()), ('link', wagtail.core.blocks.URLBlock()), ('children', wagtail.core.blocks.StreamBlock([('external_link', wagtail.core.blocks.StructBlock([('display_text', wagtail.core.blocks.CharBlock()), ('link', wagtail.core.blocks.URLBlock())])), ('page_link', wagtail.core.blocks.StructBlock([('display_text', wagtail.core.blocks.CharBlock()), ('page', wagtail.core.blocks.PageChooserBlock())]))]))])), ('page_link', wagtail.core.blocks.StructBlock([('display_text', wagtail.core.blocks.CharBlock()), ('page', wagtail.core.blocks.PageChooserBlock()), ('children', wagtail.core.blocks.StreamBlock([('external_link', wagtail.core.blocks.StructBlock([('display_text', wagtail.core.blocks.CharBlock()), ('link', wagtail.core.blocks.URLBlock())])), ('page_link', wagtail.core.blocks.StructBlock([('display_text', wagtail.core.blocks.CharBlock()), ('page', wagtail.core.blocks.PageChooserBlock())]))]))]))])),
            ],
        ),
        migrations.CreateModel(
            name='PageWithNavbar',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('navbar', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='blog.Navbar')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
