# Generated by Django 4.0 on 2022-05-03 13:30

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_post_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='body',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
