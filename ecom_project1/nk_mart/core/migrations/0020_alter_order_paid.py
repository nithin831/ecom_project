# Generated by Django 5.0 on 2024-03-07 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_alter_order_paid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='paid',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
