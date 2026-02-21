import django_filters
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import filters, serializers, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product
from .selectors import get_products_queryset
from .serializers import ProductSerializer


class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        model = Product
        fields = ["category", "is_active"]


class ProductPagination(PageNumberPagination):
    page_size = 10


class ProductListCreateAPIView(APIView):
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_class = ProductFilter
    search_fields = ["name", "description"]
    ordering_fields = ["price", "created_at"]

    pagination_class = ProductPagination

    def get_queryset(self):
        return get_products_queryset()

    def filter_queryset(self, request, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(request, queryset, self)
        return queryset

    @extend_schema(
        summary="List Products",
        responses={
            200: inline_serializer(
                name="ProductListResponse",
                fields={
                    "data": ProductSerializer(many=True),
                    "errors": serializers.DictField(allow_null=True, required=False),
                },
            )
        },
    )
    def get(self, request):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(request, queryset)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)

        serializer = ProductSerializer(page, many=True)

        return paginator.get_paginated_response({"data": serializer.data, "errors": None})

    @extend_schema(
        summary="Create Product",
        request=ProductSerializer,
        responses={
            201: inline_serializer(
                name="ProductCreateResponse",
                fields={
                    "data": ProductSerializer(),
                    "errors": serializers.DictField(allow_null=True, required=False),
                },
            ),
            400: inline_serializer(
                name="ProductCreateErrorResponse",
                fields={
                    "data": serializers.DictField(allow_null=True, required=False),
                    "errors": serializers.DictField(),
                },
            ),
        },
    )
    def post(self, request):
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"data": serializer.data, "errors": None},
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"data": None, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ProductDetailAPIView(APIView):

    def get_queryset(self):
        return get_products_queryset().filter(is_active=True)

    def get_object(self, slug):
        queryset = self.get_queryset()
        return get_object_or_404(queryset, slug=slug)

    @extend_schema(
        summary="Get Product Details",
        responses={
            200: inline_serializer(
                name="ProductDetailResponse",
                fields={
                    "data": ProductSerializer(),
                    "errors": serializers.DictField(allow_null=True, required=False),
                },
            )
        },
    )
    def get(self, request, slug):
        product = self.get_object(slug)
        serializer = ProductSerializer(product)

        return Response({"data": serializer.data, "errors": None})

    @extend_schema(
        summary="Update Product",
        request=ProductSerializer,
        responses={
            200: inline_serializer(
                name="ProductUpdateResponse",
                fields={
                    "data": ProductSerializer(),
                    "errors": serializers.DictField(allow_null=True, required=False),
                },
            ),
            400: inline_serializer(
                name="ProductUpdateErrorResponse",
                fields={
                    "data": serializers.DictField(allow_null=True, required=False),
                    "errors": serializers.DictField(),
                },
            ),
        },
    )
    def put(self, request, slug):
        product = self.get_object(slug)
        serializer = ProductSerializer(product, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "errors": None})

        return Response(
            {"data": None, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @extend_schema(
        summary="Partial Update Product",
        request=ProductSerializer,
        responses={
            200: inline_serializer(
                name="ProductPatchResponse",
                fields={
                    "data": ProductSerializer(),
                    "errors": serializers.DictField(allow_null=True, required=False),
                },
            ),
            400: inline_serializer(
                name="ProductPatchErrorResponse",
                fields={
                    "data": serializers.DictField(allow_null=True, required=False),
                    "errors": serializers.DictField(),
                },
            ),
        },
    )
    def patch(self, request, slug):
        product = self.get_object(slug)
        serializer = ProductSerializer(product, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "errors": None})

        return Response(
            {"data": None, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @extend_schema(
        summary="Delete Product",
        responses={
            204: inline_serializer(
                name="ProductDeleteResponse",
                fields={
                    "data": serializers.DictField(allow_null=True, required=False),
                    "errors": serializers.DictField(allow_null=True, required=False),
                    "message": serializers.CharField(),
                },
            )
        },
    )
    def delete(self, request, slug):
        product = self.get_object(slug)
        product.is_active = False
        product.save(update_fields=["is_active"])

        return Response(
            {
                "data": None,
                "errors": None,
                "message": "Product soft deleted successfully",
            },
            status=status.HTTP_204_NO_CONTENT,
        )
