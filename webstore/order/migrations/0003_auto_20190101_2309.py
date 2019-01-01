# Generated by Django 2.1.3 on 2019-01-01 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20181117_2055'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='edited',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['user'], name='order_order_user_id_a7f1ea_idx'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['uuid'], name='order_order_uuid_411e74_idx'),
        ),
        migrations.AddIndex(
            model_name='orderitem',
            index=models.Index(fields=['order', 'product'], name='order_order_order_i_89d10a_idx'),
        ),
        migrations.AddIndex(
            model_name='orderitem',
            index=models.Index(fields=['price'], name='order_order_price_efbc73_idx'),
        ),
    ]
