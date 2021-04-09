from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название товара')
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                verbose_name='Цена')
    description = models.TextField(blank=True, verbose_name='Описание товара')
    image = models.ImageField(blank=True, null=True,
                              upload_to='products/%Y/%m/%d',
                              verbose_name='Изображение',
                              default='default.jpg')
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Дата добавления')
    subcategory = models.ForeignKey('Subcategory',
                                    on_delete=models.CASCADE,
                                    related_name='products',
                                    verbose_name='Категория',
                                    )
    availability = models.BooleanField(default=True, verbose_name='Наличие')
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, blank=True,
                              null=True, verbose_name='Брэнд')
    color = models.ForeignKey('Color', on_delete=models.SET_NULL, null=True,
                              blank=True, verbose_name='Цвет')

    def get_absolute_url(self, ):
        return reverse('product_detail',
                       args=[self.subcategory.category.slug,
                             self.subcategory.slug, self.pk])

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['-created', ]
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Category(models.Model):
    name = models.CharField('Название категории', max_length=255)
    slug = models.SlugField('Слаг', max_length=255)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('product_by_category', args=[self.slug])

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Subcategory(models.Model):
    name = models.CharField('Подкатегория', max_length=255)
    slug = models.SlugField('Слаг', max_length=255)
    description = models.TextField('Описание', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 verbose_name='Категория')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class Brand(models.Model):
    name = models.CharField('Название брэнда', max_length=200, unique=True)
    slug = models.SlugField('Слаг', max_length=200, unique=True)
    image = models.ImageField('Изображение', upload_to='products/brand',
                              default='default.jpg',
                              blank=True, null=True)
    description = models.TextField('Описание', blank=True, null=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Брэнд'
        verbose_name_plural = 'Брэнды'

    def __str__(self):
        return f"{self.name}"


class Color(models.Model):
    name = models.CharField('Цвет', max_length=100)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'
