from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category
from .serializers import CategorySerializer


class CategoryListCreateAPIView(APIView):

    def get_queryset(self):
        return Category.objects.all().order_by("name")

    @extend_schema(
        summary="List Categories",
        responses={
            200: inline_serializer(
                name="CategoryListResponse",
                fields={
                    "data": CategorySerializer(many=True),
                    "errors": serializers.DictField(allow_null=True, required=False),
                },
            )
        },
    )
    def get(self, request):
        queryset = self.get_queryset()
        serializer = CategorySerializer(queryset, many=True)

        return Response({"data": serializer.data, "errors": None})

    @extend_schema(
        summary="Create Category",
        request=CategorySerializer,
        responses={
            201: inline_serializer(
                name="CategoryCreateResponse",
                fields={
                    "data": CategorySerializer(),
                    "errors": serializers.DictField(allow_null=True, required=False),
                },
            ),
            400: inline_serializer(
                name="CategoryCreateErrorResponse",
                fields={
                    "data": serializers.DictField(allow_null=True, required=False),
                    "errors": serializers.DictField(),
                },
            ),
        },
    )
    def post(self, request):
        serializer = CategorySerializer(data=request.data)

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


class CategoryDetailAPIView(APIView):

    def get_queryset(self):
        return Category.objects.all()

    def get_object(self, slug):
        queryset = self.get_queryset()
        return get_object_or_404(queryset, slug=slug)

    @extend_schema(
        summary="Get Category Details",
        responses={
            200: inline_serializer(
                name="CategoryDetailResponse",
                fields={
                    "data": CategorySerializer(),
                    "errors": serializers.DictField(allow_null=True, required=False),
                },
            )
        },
    )
    def get(self, request, slug):
        category = self.get_object(slug)
        serializer = CategorySerializer(category)

        return Response({"data": serializer.data, "errors": None})

    @extend_schema(
        summary="Update Category",
        request=CategorySerializer,
        responses={
            200: inline_serializer(
                name="CategoryUpdateResponse",
                fields={
                    "data": CategorySerializer(),
                    "errors": serializers.DictField(allow_null=True, required=False),
                },
            ),
            400: inline_serializer(
                name="CategoryUpdateErrorResponse",
                fields={
                    "data": serializers.DictField(allow_null=True, required=False),
                    "errors": serializers.DictField(),
                },
            ),
        },
    )
    def put(self, request, slug):
        category = self.get_object(slug)
        serializer = CategorySerializer(category, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "errors": None})

        return Response(
            {"data": None, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @extend_schema(
        summary="Partial Update Category",
        request=CategorySerializer,
        responses={
            200: inline_serializer(
                name="CategoryPatchResponse",
                fields={
                    "data": CategorySerializer(),
                    "errors": serializers.DictField(allow_null=True, required=False),
                },
            ),
            400: inline_serializer(
                name="CategoryPatchErrorResponse",
                fields={
                    "data": serializers.DictField(allow_null=True, required=False),
                    "errors": serializers.DictField(),
                },
            ),
        },
    )
    def patch(self, request, slug):
        category = self.get_object(slug)
        serializer = CategorySerializer(category, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "errors": None})

        return Response(
            {"data": None, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "errors": None})

        return Response(
            {"data": None, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @extend_schema(
        summary="Delete Category",
        responses={
            204: inline_serializer(
                name="CategoryDeleteResponse",
                fields={
                    "data": serializers.DictField(allow_null=True, required=False),
                    "errors": serializers.DictField(allow_null=True, required=False),
                    "message": serializers.CharField(),
                },
            )
        },
    )
    def delete(self, request, slug):
        category = self.get_object(slug)
        category.delete()

        return Response(
            {"data": None, "errors": None, "message": "Category deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
