from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.http import Http404

from rest_framework.views import APIView
from django.views.generic.list import ListView 
from rest_framework.generics import ListCreateAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from .models import Product
from .serializers import ProductSerializer
from .paginations import CustomNumberPagination

import json

class ProductList(APIView):
    pagination_class = CustomNumberPagination
    def get(self, request, *args, **kwargs):
        paginator = self.pagination_class()

        product_name = request.GET.get('name', None)

        min_price = request.GET.get('min_price', 0)
        max_price = request.GET.get('max_price', 99999999999999999)
        
        if product_name:                         # Check if there is a get parameter called 'name' (/?name=xxxx&...)
            products = Product.objects.filter(price__range=(min_price, max_price), name__exact=product_name)   # Get the object in database
            page = paginator.paginate_queryset(products, request)

            if page is not None:
                serializer = ProductSerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)
            
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

        else:
            products = Product.objects.filter(price__range=(min_price, max_price))

            page = paginator.paginate_queryset(products, request)

            if page is not None:
                serializer = ProductSerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)

            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)

    def post(self, request):
        product = request.data
            
        serializer = ProductSerializer(data=product)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProductDetail(APIView):
    def get_object(self, id):
        try:
            return Product.objects.get(pk=id)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        serializer = ProductSerializer(self.get_object(id))
        return Response(serializer.data)
        
    def patch(self, request, id, format=None):
        serializer = ProductSerializer(self.get_object(id), data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id, format=None):

        serializer = ProductSerializer(self.get_object(id), data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, id, format=None):

        self.get_object(id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

        
# class ProductFilter(APIView):
    