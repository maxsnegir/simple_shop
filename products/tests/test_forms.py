import shutil
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse

from products.forms import CreateProduct
from products.models import Category, Product, Subcategory

User = get_user_model()


class ProductTestForms(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаем временную папку для медиа-файлов;
        # на момент теста медиа папка будет перопределена
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
        cls.category = Category.objects.create(name='Обувь', slug='shoes')
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
        cls.form = CreateProduct()

    @classmethod
    def tearDownClass(cls):
        # Модуль shutil - библиотека Python с инструментами
        # для управления файлами и директориями:
        # создание, удаление, копирование, перемещение, изменение папок|файлов
        # Метод shutil.rmtree удаляет директорию и всё её содержимое
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.moderator = User.objects.create_user(username='username',
                                                  role='moderator')
        self.authorized_moderator = Client()
        self.authorized_moderator.force_login(self.moderator)

    def test_create_product_form(self):
        """
        Проверка коректности формы добавления товара
        """
        create_product = reverse('create_product')
        products_count = Product.objects.count()

        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )

        form_data = {
            'name': 'Новый',
            'price': 121,
            'description': 'Описание товара',
            'image': uploaded,
            'subcategory': self.subcategory.id,
            'availability': True,
        }

        response = self.authorized_moderator.post(create_product,
                                                  data=form_data,
                                                  follow=True)
        self.assertRedirects(response, reverse('product_detail',
                                               args=[self.category.slug,
                                                     self.subcategory.slug,
                                                     2]))

        self.assertEqual(Product.objects.count(), products_count + 1)

        self.assertTrue(Product.objects.filter(
            name='Новый', price=121, subcategory=self.subcategory.id,
            availability=True).exists())
