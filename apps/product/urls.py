from django.urls import path

from .views import ProductDetail, ProductList

urlpatterns = [
    path("products/", ProductList.as_view(), name="products_list"),
    path("products/<str:product_id>",
         ProductDetail.as_view(), name="products_details"),
]
