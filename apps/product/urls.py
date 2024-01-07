from django.urls import path

from .views import ProductList, ProductDetail

urlpatterns = [
    path("products/", ProductList.as_view(), name="products_list"),
    path("products/<str:id>", ProductDetail.as_view(),
         name="products_details"),
]
