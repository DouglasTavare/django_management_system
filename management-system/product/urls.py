from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('products/', views.manage_products, name='manage_products'),
    # path('products/', views.post_product, name='post_product'),
    path('products/<str:id>', views.get_by_id),
    # path('data/', views.product_manager)
]