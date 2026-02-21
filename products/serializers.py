from rest_framework import serializers

from categories.models import Category

from .models import Product
from .services import create_product, update_product


class ProductSerializer(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Category.objects.all(),
        required=False,
        allow_null=True,
    )

    category_name = serializers.CharField(source="category.name", read_only=True)

    slug = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "price",
            "stock",
            "category",
            "category_name",
            "image",
            "thumbnail",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "thumbnail",
            "created_at",
            "updated_at",
            "is_active",
        ]

    def create(self, validated_data):
        return create_product(**validated_data)

    def update(self, instance, validated_data):
        return update_product(instance, **validated_data)


class ProductWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Category.objects.all(),
        required=False,
        allow_null=True,
    )
    slug = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Product
        fields = [
            "name",
            "slug",
            "description",
            "price",
            "stock",
            "category",
            "image",
            "is_active",
        ]
        ref_name = "ProductWrite"

    def create(self, validated_data):
        return create_product(**validated_data)

    def update(self, instance, validated_data):
        return update_product(instance, **validated_data)
