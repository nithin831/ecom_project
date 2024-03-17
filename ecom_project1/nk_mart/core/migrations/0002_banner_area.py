# Generated by Django 5.0 on 2024-02-09 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner_area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Image', models.ImageField(upload_to='media/banner_imgs')),
                ('Discount_deal', models.CharField(max_length=100)),
                ('Quote', models.CharField(max_length=200)),
                ('Discount', models.IntegerField()),
            ],
        ),
    ]
