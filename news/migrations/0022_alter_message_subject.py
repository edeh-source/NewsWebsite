# Generated by Django 5.0.4 on 2024-08-29 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0021_alter_category_options_alter_post_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='subject',
            field=models.CharField(max_length=256),
        ),
    ]
