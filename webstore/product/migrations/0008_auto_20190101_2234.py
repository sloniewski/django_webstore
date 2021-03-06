# Generated by Django 2.1.3 on 2019-01-01 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_auto_20190101_2222'),
    ]

    operations = [
        migrations.RenameField(
            model_name='picture',
            old_name='modified',
            new_name='edited',
        ),
        migrations.RemoveField(
            model_name='product',
            name='height',
        ),
        migrations.RemoveField(
            model_name='product',
            name='length',
        ),
        migrations.RemoveField(
            model_name='product',
            name='width',
        ),
        migrations.AddIndex(
            model_name='gallery',
            index=models.Index(fields=['product'], name='product_gal_product_cf8f39_idx'),
        ),
        migrations.AddIndex(
            model_name='gallery',
            index=models.Index(fields=['picture'], name='product_gal_picture_7c7096_idx'),
        ),
        migrations.AddIndex(
            model_name='price',
            index=models.Index(fields=['product'], name='product_pri_product_8ccd98_idx'),
        ),
    ]
