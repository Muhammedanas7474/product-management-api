from .models import Product


def get_products_queryset():
    return Product.objects.select_related("category").order_by("-created_at")
