# Generated by Django 5.0 on 2024-01-06 09:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_alter_item_shop_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='shop_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.shop'),
        ),
    ]
