from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Category
from .serializers import CategorySerializer


class CategoryListCreateAPIView(APIView):

    def get_queryset(self):
        return Category.objects.all().order_by("name")

    def get(self, request):
        queryset = self.get_queryset()
        serializer = CategorySerializer(queryset, many=True)

        return Response({
            "data": serializer.data,
            "errors": None
        })

    def post(self, request):
        serializer = CategorySerializer(data=request.data)

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


class CategoryDetailAPIView(APIView):

    def get_queryset(self):
        return Category.objects.all()

    def get_object(self, slug):
        queryset = self.get_queryset()
        return get_object_or_404(queryset, slug=slug)

    def get(self, request, slug):
        category = self.get_object(slug)
        serializer = CategorySerializer(category)

        return Response({
            "data": serializer.data,
            "errors": None
        })

    def put(self, request, slug):
        category = self.get_object(slug)
        serializer = CategorySerializer(category, data=request.data, partial=True)

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
        category = self.get_object(slug)
        category.delete()

        return Response(
            {
                "data": None,
                "errors": None,
                "message": "Category deleted successfully"
            },
            status=status.HTTP_204_NO_CONTENT
        )
