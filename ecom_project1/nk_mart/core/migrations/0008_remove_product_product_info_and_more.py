# Generated by Django 5.0 on 2024-02-10 05:36

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_additional_info_detail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='Product_info',
        ),
        migrations.AddField(
            model_name='product',
            name='Product_information',
            field=ckeditor.fields.RichTextField(default='nk'),
        ),
        migrations.AlterField(
            model_name='product',
            name='Description',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
