# Generated by Django 5.0 on 2024-02-14 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_product_packing_cost_product_tax'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon_code',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('discount', models.IntegerField()),
            ],
        ),
    ]
