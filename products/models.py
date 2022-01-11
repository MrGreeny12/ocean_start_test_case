import datetime

from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from products.managers import ProductManager


class Category(models.Model):
    '''
    Модель категории товаров
    '''
    title = models.CharField(max_length=512, verbose_name='Название')

    @classmethod
    def get_or_create(cls, title: str):
        try:
            category = cls.objects.get(title=title)
            return category
        except ObjectDoesNotExist:
            category = cls.objects.create(title=title)
            return category

    def __str__(self):
        return self.title

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'categories'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    '''
    Модель товара
    '''
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name='Удален')
    deleted = models.BooleanField(default=False, verbose_name='Помечен на удаление')
    title = models.CharField(max_length=512, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    price = models.IntegerField(verbose_name='Цена')
    categories = models.ManyToManyField(
        Category,
        related_name='products',
        verbose_name='Категории'
    )
    public = models.BooleanField(default=True, verbose_name='Опубликован')

    active = ProductManager()

    @classmethod
    def safety_delete(cls, product_id: int):
        product = cls.active.get(id=product_id)
        product.deleted = True
        product.deleted_at = datetime.datetime.now()
        product.public = False
        product.save()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'products'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
