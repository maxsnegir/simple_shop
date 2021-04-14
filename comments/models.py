from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from products.models import Product

User = get_user_model()


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='comments',
                                verbose_name='Товар')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='comments', verbose_name='Автор')
    text = models.TextField('Текст комментария')
    created = models.DateTimeField('Дата создания', auto_now_add=True, )

    def get_absolute_url(self):
        return reverse('add_comment',
                       args=[self.product.subcategory.category.slug,
                             self.product.subcategory.slug, self.product.pk])

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий от {self.author}'
