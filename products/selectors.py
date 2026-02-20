from .models import Product


def get_products_queryset():
    return (
        Product.objects
        .select_related("category")
        .filter(is_active=True)
        .order_by("-created_at")
    )
