# Generated by Django 2.1.3 on 2019-01-06 20:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_auto_20190101_2234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='picture',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='products', to='product.Picture'),
        ),
        migrations.AlterField(
            model_name='gallery',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='gallery', to='product.Product'),
        ),
    ]
