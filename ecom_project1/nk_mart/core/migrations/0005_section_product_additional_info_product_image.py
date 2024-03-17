# Generated by Django 5.0 on 2024-02-09 18:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_main_category_category_sub_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_quantity', models.IntegerField()),
                ('availability', models.IntegerField()),
                ('featured_image', models.CharField(max_length=100)),
                ('product_name', models.CharField(max_length=50)),
                ('price', models.IntegerField()),
                ('Discount', models.IntegerField()),
                ('Product_info', models.TextField()),
                ('model_name', models.CharField(max_length=50)),
                ('Tags', models.CharField(max_length=100)),
                ('Description', models.TextField()),
                ('Categories', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.category')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.section')),
            ],
        ),
        migrations.CreateModel(
            name='Additional_info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specification', models.CharField(max_length=100)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.product')),
            ],
        ),
        migrations.CreateModel(
            name='Product_image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.CharField(max_length=200)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.product')),
            ],
        ),
    ]
