from django_filters import rest_framework as filters

from products.models import Product, Category


class ProductsFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    categories_id = filters.Filter(field_name='categories')
    categories_title = filters.CharFilter(field_name='categories__title', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ('title', 'min_price', 'max_price', 'categories_id', 'categories_title', 'public', 'deleted')
