from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Product
from .serializers import ProductSerializer

import json

class ProductList(APIView):
    def get(self, request):

        products = Product.objects.all()
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
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id, format=None):

        serializer = ProductSerializer(self.get_object(id), data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, id, format=None):

        self.get_object(id).delete()
        return Response(status=status.HTTP_202_ACCEPTED)