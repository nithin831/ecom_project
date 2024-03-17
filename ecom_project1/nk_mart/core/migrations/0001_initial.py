# Generated by Django 5.0 on 2024-02-08 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Image', models.ImageField(upload_to='media/slider_imgs')),
                ('Discount_deal', models.CharField(choices=[('HOT DEALS', 'HOT DEALS'), ('NEW ARRIVALS', 'NEW ARRIVALS')], max_length=100)),
                ('Sale', models.IntegerField()),
                ('Brand_name', models.CharField(max_length=200)),
                ('Discount', models.IntegerField()),
                ('Link', models.CharField(max_length=200)),
            ],
        ),
    ]
