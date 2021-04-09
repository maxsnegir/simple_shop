from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django import forms
from products.models import Category, Product, Subcategory

User = get_user_model()


class ProductViewsTest(TestCase):

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

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create(username='username',
                                        role='moderator')
        self.authorized_client = Client(self.user)
        self.authorized_client.force_login(self.user)

    def test_context_index(self):
        """
        Тест правильности передоваемого коннтекста на страницу index
        """
        index = reverse('index')
        response = self.guest_client.get(index)
        for product in response.context['products']:
            with self.subTest():
                self.assertIsInstance(product, Product)

    def test_context_product_detail(self):
        """
        Тест правильности передоваемого коннтекста на страницу product_detail
        """
        product_detail = reverse('product_detail',
                                 args=[self.category.slug,
                                       self.subcategory.slug, self.product.id])
        response = self.guest_client.get(product_detail)
        self.assertIsInstance(response.context['product'], Product)

    def test_context_products_by_category(self):
        """
        Тест правильности передоваемого коннтекста на страницу product_by_category
        """
        products_by_category = reverse('product_by_category',
                                       args=[self.category.slug])
        response = self.guest_client.get(products_by_category)
        for product in response.context['products']:
            with self.subTest():
                self.assertIs(self.product.subcategory, self.subcategory)
                self.assertIsInstance(product, Product)

    def test_context_create_product(self):
        """
        Тест правильности передоваемого коннтекста на страницу create_product
        """
        create_product = reverse('create_product')
        response = self.authorized_client.get(create_product)
        form_fields = {
            'name': forms.fields.CharField,
            'price': forms.fields.DecimalField,
            'brand': forms.fields.ChoiceField,
            'description': forms.fields.CharField,
            'subcategory': forms.fields.ChoiceField,
            'color': forms.fields.ChoiceField,
            'image': forms.fields.ImageField,
            'availability': forms.fields.BooleanField,
        }

        for field, expected in form_fields.items():
            with self.subTest():
                self.assertIsInstance(
                    response.context['form'].fields[field], expected)
