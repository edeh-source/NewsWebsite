# Generated by Django 5.0.4 on 2024-09-05 21:02

import django_resized.forms
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0023_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=85, scale=None, size=[900, 900], upload_to='post_images'),
        ),
    ]
