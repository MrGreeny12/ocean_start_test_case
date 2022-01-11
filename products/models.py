from django.db import models


class Category(models.Model):
    '''
    Модель категории товаров
    '''
    title = models.CharField(max_length=512, verbose_name='Название')

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
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name='Помечен на удаление')
    title = models.CharField(max_length=512, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    price = models.IntegerField(verbose_name='Цена')
    categories = models.ManyToManyField(
        Category,
        related_name='products',
        verbose_name='Категории'
    )
    public = models.BooleanField(default=True, verbose_name='Опубликован')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'products'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
