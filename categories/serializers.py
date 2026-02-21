from rest_framework import serializers
from slugify import slugify

from .models import Category


class CategorySerializer(serializers.ModelSerializer):

    slug = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def create(self, validated_data):
        if not validated_data.get("slug"):
            validated_data["slug"] = slugify(validated_data["name"])
        return super().create(validated_data)
