# Generated by Django 5.0.4 on 2024-08-22 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0020_author_about_author_email'),
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['-created', '-id'], 'verbose_name': 'category', 'verbose_name_plural': 'categories'},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created']},
        ),
        migrations.AddIndex(
            model_name='category',
            index=models.Index(fields=['-created', '-id'], name='news_catego_created_df5dba_idx'),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['-created', '-id'], name='news_post_created_0d4aaf_idx'),
        ),
    ]
