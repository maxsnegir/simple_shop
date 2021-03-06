# Generated by Django 3.1.7 on 2021-04-14 13:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20210404_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Название категории'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=255, unique=True, verbose_name='Слаг'),
        ),
        migrations.AlterField(
            model_name='color',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Цвет'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0, 'Цена не может быть меньше 0')], verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Подкатегория'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='slug',
            field=models.SlugField(max_length=255, unique=True, verbose_name='Слаг'),
        ),
    ]
