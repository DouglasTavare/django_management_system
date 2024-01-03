from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Product
from .serializers import ProductSerializer

import json
# Create your views here.

@api_view(['GET', 'POST'])
def manage_products(request):

    if request.method == 'GET':

        products = Product.objects.all()                          # Get all objects in User's database (It returns a queryset)

        serializer = ProductSerializer(products, many=True)       # Serialize the object data into json (Has a 'many' parameter cause it's a queryset)

        return Response(serializer.data)                    # Return the serialized data
    
    if request.method == 'POST':

        product = request.data
        
        serializer = ProductSerializer(data=product)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def get_by_id(request, id):

    try:
        product = Product.objects.get(pk=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':

        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    if request.method == 'PATCH':
        serializer = ProductSerializer(product, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':

        serializer = ProductSerializer(product, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':

        try:
            product.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
# @api_view(['POST'])
# def post_product(request):
#     if request.method == 'POST':

#         product = request.data
        
#         serializer = ProductSerializer(data=product)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
    
#         return Response(status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET','POST','PUT','DELETE'])
# def product_manager(request):
#     if request.method == 'GET':

#         try:
#             if request.GET['name']:                         # Check if there is a get parameter called 'name' (/?name=xxxx&...)

#                 product_name = request.GET['name']         # Find get parameter

#                 try:
#                     product = Product.objects.get(name=product_name)   # Get the object in database
#                 except:
#                     return Response(status=status.HTTP_404_NOT_FOUND)

#                 serializer = ProductSerializer(product)           # Serialize the object data into json
#                 return Response(serializer.data)            # Return the serialized data

#             else:
#                 return Response(status=status.HTTP_400_BAD_REQUEST)
            
#         except:
#             return Response(status=status.HTTP_400_BAD_REQUEST)






# EDITAR DADOS (PUT)

    # if request.method == 'PUT':

    #     name = request.data['product']

    #     try:
    #         updated_user = Product.objects.get(pk=name)
    #     except:
    #         return Response(status=status.HTTP_404_NOT_FOUND)

        
    #     print('Resultado final ', fn.soma(1,2))

    #     serializer = ProductSerializer(updated_user, data=request.data)

    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        
    #     return Response(status=status.HTTP_400_BAD_REQUEST)