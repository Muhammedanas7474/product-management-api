import uuid
from slugify import slugify
from .models import Product


def generate_unique_slug(name: str, instance=None) -> str:
    base_slug = slugify(name)
    slug = base_slug

    queryset = Product.objects.all()

    if instance:
        queryset = queryset.exclude(pk=instance.pk)

    counter = 1
    while queryset.filter(slug=slug).exists():
        short_suffix = uuid.uuid4().hex[:6]
        slug = f"{base_slug}-{short_suffix}"
        counter += 1

    return slug
