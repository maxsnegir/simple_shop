from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from products.models import Category, Product, Subcategory

User = get_user_model()


class StaticURLTest(TestCase):

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
        self.user = User.objects.create(username='username')
        self.moderator = User.objects.create(username='username_2',
                                             role='moderator')
        self.authorized_client = Client()
        self.authorized_moderator = Client()
        self.authorized_moderator = Client(self.moderator)
        self.authorized_client.force_login(self.user)
        self.authorized_moderator.force_login(self.moderator)

    def test_homepage(self):
        """
        Тест доступности страницы index
        """
        homepage = reverse('index')
        response = self.guest_client.get(homepage)
        self.assertEqual(response.status_code, 200)

    def test_category_page(self):
        """
        Тест доступности страницы товаров по определенной категории
        """
        category_page = self.category.get_absolute_url()
        response = self.guest_client.get(category_page)
        self.assertEqual(response.status_code, 200)

    def test_product_page(self):
        """
        Тест доступности страницы определенного товара
        """
        product_page = self.product.get_absolute_url()
        response = self.guest_client.get(product_page)
        self.assertEqual(response.status_code, 200)

    def test_create_product_page_redirect_unauthorized_and_user(self):
        """
        Тест доступности страницы create_product для не авторизованного и для
        обычного пользователя
        """
        create_product = reverse('create_product')
        response_unauthorized = self.guest_client.get(create_product,
                                                      follow=True)
        response_authorized = self.authorized_client.get(create_product,
                                                         follow=True)
        self.assertRedirects(response_unauthorized, reverse('index'))
        self.assertRedirects(response_authorized, reverse('index'))

    def test_create_product_page_for_moderator(self):
        """
        Тест доступности страницы create_product для модератора или админа
        """
        create_product = reverse('create_product')
        response = self.authorized_moderator.get(create_product)
        self.assertEqual(response.status_code, 200)

    def test_urls_correct_template(self):
        """
        Тест шаблонов
        """
        templates = {
            'products/products_list.html': reverse('index'),
            'products/product_detail.html': reverse('product_detail',
                                                    args=[self.category.slug,
                                                          self.subcategory.slug,
                                                          self.product.pk]),
            'products/product_by_category.html': reverse('product_by_category',
                                                         args=[
                                                             self.category.slug]),
            'products/create_product.html': reverse('create_product'),
        }
        for path, url in templates.items():
            with self.subTest():
                response = self.authorized_moderator.get(url)
                self.assertTemplateUsed(response, path)
