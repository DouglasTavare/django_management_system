"""
Module containing views for handling Product-related operations in the 'products' application.

This module includes Django and Django Rest Framework views for listing and managing products.
The views are designed to handle CRUD (Create, Read, Update, Delete) operations for the 'Product' model.

Classes:
- ProductList(APIView): A view class for listing and creating products.
- ProductDetail(APIView): A view class for retrieving, updating, and deleting a specific product.

Permissions:
- Both views require authentication, and 'IsAuthenticated' permission is enforced.

Attributes:
- pagination_class (class): Custom pagination class ('CustomNumberPagination') used in ProductList.

Methods:
- ProductList.get(request): Handles GET requests for listing products.
- ProductList.post(request): Handles POST requests for creating a new product.

- ProductDetail.get(request, id): Handles GET requests for retrieving a specific product.
- ProductDetail.patch(request, id): Handles PATCH requests for partially updating a product.
- ProductDetail.put(request, id): Handles PUT requests for updating a product.
- ProductDetail.delete(request, id): Handles DELETE requests for deleting a product.

Note: Detailed method descriptions and attribute explanations are provided within each class and method.
"""
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Product
from .serializers import ProductSerializer
from .paginations import CustomNumberPagination


class ProductList(APIView):
    """
    View for listing and creating products.

    This view supports both listing all products and creating a new product.
    Authentication is required, and 'IsAuthenticated' permission is enforced.

    Attributes:
    - permission_classes (tuple): Tuple specifying required permissions (IsAuthenticated).
    - pagination_class (class): Custom pagination class ('CustomNumberPagination').

    Methods:
    - get(request): Handles GET requests for listing products.
    - post(request): Handles POST requests for creating a new product.
    """
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomNumberPagination

    def get(self, request):
        """
        Handle GET requests for listing products.

        Parameters:
        - request (HttpRequest): The HTTP request object.

        Returns:
        - Response: JSON response containing the serialized product data.
        """
        paginator = self.pagination_class()

        product_name = request.GET.get("name", None)

        min_price = request.GET.get("min_price", 0)
        max_price = request.GET.get("max_price", 99999999999999999)

        if (
            product_name
        ):
            products = Product.objects.filter(
                price__range=(min_price, max_price), name__exact=product_name
            )
            page = paginator.paginate_queryset(products, request)

            if page is not None:
                serializer = ProductSerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

        else:
            products = Product.objects.filter(
                price__range=(min_price, max_price))

            page = paginator.paginate_queryset(products, request)

            if page is not None:
                serializer = ProductSerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)

            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)

    def post(self, request):
        """
        Handle POST requests for creating a new product.

        Parameters:
        - request (HttpRequest): The HTTP request object.

        Returns:
        - Response: JSON response containing the serialized product data or error messages.
        """
        product = request.data

        serializer = ProductSerializer(data=product)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetail(APIView):
    """
    View for retrieving, updating, and deleting a specific product.

    This view supports retrieving, updating, and deleting a specific product identified by 'id'.
    Authentication is required, and 'IsAuthenticated' permission is enforced.

    Attributes:
    - permission_classes (tuple): Tuple specifying required permissions (IsAuthenticated).

    Methods:
    - get_object(id): Helper method to retrieve a Product instance based on the provided 'id'.
    - get(request, id): Handles GET requests for retrieving a specific product.
    - patch(request, id): Handles PATCH requests for partially updating a product.
    - put(request, id): Handles PUT requests for updating a product.
    - delete(request, id): Handles DELETE requests for deleting a product.
    """
    permission_classes = (IsAuthenticated,)

    def get_object(self, id):
        """
        Retrieve a Product instance based on the provided 'id'.

        Parameters:
        - id (str): The unique identifier of the product.

        Returns:
        - Product: The retrieved Product instance.

        Raises:
        - Http404: If the product with the specified 'id' does not exist.
        """
        try:
            return Product.objects.get(pk=id)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, id):
        """
        Handle GET requests for retrieving a specific product.

        Parameters:
        - request (HttpRequest): The HTTP request object.
        - id (str): The unique identifier of the product.

        Returns:
        - Response: JSON response containing the serialized product data or an error message.
        """
        serializer = ProductSerializer(self.get_object(id))
        return Response(serializer.data)

    def patch(self, request, id):
        """
        Handle PATCH requests for partially updating a product.

        Parameters:
        - request (HttpRequest): The HTTP request object.
        - id (str): The unique identifier of the product.

        Returns:
        - Response: JSON response containing the updated product data or an error message.
        """
        serializer = ProductSerializer(
            self.get_object(id), data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        """
        Handle PUT requests for updating a product.

        Parameters:
        - request (HttpRequest): The HTTP request object.
        - id (str): The unique identifier of the product.

        Returns:
        - Response: JSON response containing the updated product data or an error message.
        """
        serializer = ProductSerializer(self.get_object(id), data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        """
        Handle DELETE requests for deleting a product.

        Parameters:
        - request (HttpRequest): The HTTP request object.
        - id (str): The unique identifier of the product.

        Returns:
        - Response: Empty response with status code indicating success or failure.
        """
        self.get_object(id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
