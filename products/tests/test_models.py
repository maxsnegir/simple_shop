from django.test import TestCase
from ..models import Product, Category, Subcategory


class ProductModelTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = Category.objects.create(
            name='Обувь',
            slug='shoes'
        )

        cls.subcategory = Subcategory.objects.create(
            name='Кроссовки',
            slug='sneakers',
            description='Описание подкатегории',
            category=cls.category
        )
        cls.product = Product.objects.create(
            name='Товар',
            price=123,
            description='Это описание',
            subcategory=cls.subcategory
        )

    def test_verbose_name(self):
        """
        Проверка коректности полей verbose_name в модели Product
        """
        product = self.product
        verbose_fields = {
            'name': 'Название товара',
            'price': 'Цена',
            'description': 'Описание товара',
            'image': 'Изображение',
            'created': 'Дата добавления',
            'subcategory': 'Категория',
            'availability': 'Наличие',
            'color': 'Цвет',
            'brand': 'Брэнд'
        }

        for value, expected in verbose_fields.items():
            with self.subTest(value=value):
                self.assertEqual(product._meta.get_field(value).verbose_name,
                                 expected)

    def test_str_method(self):
        """Тест метода __str__ в модели Product"""
        product = self.product
        self.assertEqual(product.__str__(), product.name)
