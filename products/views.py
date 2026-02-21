from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, filters
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema

from .models import Product
from .serializers import ProductSerializer
from .selectors import get_products_queryset


class ProductPagination(PageNumberPagination):
    page_size = 10


class ProductListCreateAPIView(APIView):
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = ["category"]
    search_fields = ["name", "description"]
    ordering_fields = ["price", "created_at"]

    pagination_class = ProductPagination

    def get_queryset(self):
        return get_products_queryset().filter(is_active=True)

    def filter_queryset(self, request, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(request, queryset, self)
        return queryset

    def get(self, request):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(request, queryset)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)

        serializer = ProductSerializer(page, many=True)

        return paginator.get_paginated_response({
            "data": serializer.data,
            "errors": None
        })


    
    def post(self, request):
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "data": serializer.data,
                    "errors": None
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                "data": None,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class ProductDetailAPIView(APIView):

    def get_queryset(self):
        return get_products_queryset().filter(is_active=True)

    def get_object(self, slug):
        queryset = self.get_queryset()
        return get_object_or_404(queryset, slug=slug)

    def get(self, request, slug):
        product = self.get_object(slug)
        serializer = ProductSerializer(product)

        return Response({
            "data": serializer.data,
            "errors": None
        })

    def put(self, request, slug):
        product = self.get_object(slug)
        serializer = ProductSerializer(product, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "errors": None
            })

        return Response(
            {
                "data": None,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, slug):
        product = self.get_object(slug)
        product.is_active = False
        product.save(update_fields=["is_active"])

        return Response(
            {
                "data": None,
                "errors": None,
                "message": "Product soft deleted successfully"
            },
            status=status.HTTP_204_NO_CONTENT
        )
