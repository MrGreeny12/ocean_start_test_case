from rest_framework import serializers

from products.models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductsSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)

    def create(self, validated_data):
        categories_data = validated_data.pop('categories')
        if (2 > len(categories_data)) or (len(categories_data) > 10):
            raise serializers.ValidationError("У каждого товара может быть от 2х до 10 категорий")
        product = Product.active.create(**validated_data)
        for category_data in categories_data:
            category = Category.objects.get_or_create(**category_data)
            product.categories.add(category[0])
            product.save()
        return product

    class Meta:
        model = Product
        fields = '__all__'
