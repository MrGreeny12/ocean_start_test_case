from django.urls import path

from .versions.v1_0.views import ProductsAPIView, ProductAPIView, CategoriesAPIView, CategoryAPIView


urlpatterns = [
    path('products/', ProductsAPIView.as_view(), name='products'),
    path('product/<int:id>', ProductAPIView.as_view(), name='product'),
    path('categories/', CategoriesAPIView.as_view(), name='categories'),
    path('category/<int:id>', CategoryAPIView.as_view(), name='category')
]
