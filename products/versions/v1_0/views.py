from rest_framework import generics, status
from rest_framework.response import Response
from django_filters import rest_framework as filters
from django.core.exceptions import ObjectDoesNotExist

from products.models import Product, Category
from products.versions.v1_0.filters import ProductsFilter
from products.versions.v1_0.serializers import ProductsSerializer, CategorySerializer


class ProductsAPIView(generics.ListCreateAPIView):
    '''
    API (v1.0) для создания товара (метод POST) и получения списка товаров (метод GET)
    '''
    queryset = Product.active.all()
    serializer_class = ProductsSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductsFilter


class ProductAPIView(generics.RetrieveUpdateDestroyAPIView):
    '''
    API (v1.0) для просмотра, изменения и удаления товара
    '''
    queryset = Product.active.all()
    serializer_class = ProductsSerializer
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            Product.safety_delete(product_id=instance.id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CategoriesAPIView(generics.CreateAPIView):
    '''
    API (v1.0) для создания категории товара
    '''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryAPIView(generics.RetrieveUpdateDestroyAPIView):
    '''
    API (v1.0) для просмотра, редактирования и удаления категории товара
    '''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if len(instance.products.all()) > 0:
                return Response(data={"error": "У категории имеется 1 или более товаров. Удалите данные о товарах "
                                               "категории и повторите попытку."},
                                status=status.HTTP_409_CONFLICT)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
