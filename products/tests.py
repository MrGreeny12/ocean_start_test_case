from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from products.models import Product, Category
from products.versions.v1_0.serializers import ProductsSerializer


client = Client()


class TestProductAPI(TestCase):
    def setUp(self) -> None:
        self.product_1 = Product(
            title='Продукт 1',
            description='-',
            price=12022
        )
        self.product_1.save()
        self.product_2 = Product(
            title='Продукт 2',
            description='-',
            price=50000
        )
        self.product_2.save()
        self.category_1 = Category.objects.create(title='Категория 1')
        self.category_2 = Category.objects.create(title='Категория 2')
        self.category_3 = Category.objects.create(title='Категория 3')
        self.category_4 = Category.objects.create(title='Категория 4')
        self.category_5 = Category.objects.create(title='Категория 5')
        self.product_1.categories.add(self.category_1)
        self.product_1.categories.add(self.category_2)
        self.product_1.categories.add(self.category_3)
        self.product_2.categories.add(self.category_3)
        self.product_2.categories.add(self.category_4)
        self.product_2.categories.add(self.category_5)

    def test_get_all_products(self):
        response = client.get(reverse('products_1_0:products'))
        products = Product.active.all()
        serializer = ProductsSerializer(products, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_undeleted_products(self):
        Product.safety_delete(product_id=self.product_1.pk)
        response = client.get(reverse('products_1_0:products'), data={"deleted": False})
        products = Product.active.filter(deleted=False)
        serializer = ProductsSerializer(products, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_category_id_filter(self):
        response = client.get(reverse('products_1_0:products'), data={"categories_id": 3})
        products = Product.active.filter(categories__id=3)
        serializer = ProductsSerializer(products, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_category_title_filter(self):
        response = client.get(reverse('products_1_0:products'), data={"categories_title": 'Категория 3'})
        products = Product.active.filter(categories__title='Категория 3')
        serializer = ProductsSerializer(products, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_public_products(self):
        response = client.get(reverse('products_1_0:products'), data={"public": True})
        products = Product.active.filter(public=True)
        serializer = ProductsSerializer(products, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_products_in_price_range(self):
        response = client.get(reverse('products_1_0:products'), data={
            "min_price": 30000,
            "max_price": 50000
        })
        products = Product.active.filter(price__gte=50000, price__gt=30000)
        serializer = ProductsSerializer(products, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_product_by_title(self):
        response = client.get(reverse('products_1_0:products'), data={"title": "Продукт 1"})
        products = Product.active.filter(title="Продукт 1")
        serializer = ProductsSerializer(products, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
