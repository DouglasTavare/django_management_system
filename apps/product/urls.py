from django.urls import path

from . import views

urlpatterns = [
    path("products/", views.ProductList.as_view(), name="products_list"),
    path("products/<str:id>", views.ProductDetail.as_view(),
         name="products_details"),
]
