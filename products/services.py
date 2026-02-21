from .models import Product
from .tasks import generate_thumbnail
from .utils import generate_unique_slug


def create_product(**validated_data):
    slug = validated_data.get("slug")

    # Handle None OR empty string properly
    if not slug or slug.strip() == "":
        validated_data["slug"] = generate_unique_slug(validated_data["name"])

    product = Product.objects.create(**validated_data)

    # Dispatch async thumbnail
    if product.image:
        generate_thumbnail.delay(str(product.id))

    return product


def update_product(instance: Product, **validated_data):
    slug = validated_data.get("slug")
    name_changed = False

    if "name" in validated_data and validated_data["name"] != instance.name:
        name_changed = True

    # If slug not provided OR blank and name changed → regenerate
    if (not slug or slug.strip() == "") and name_changed:
        validated_data["slug"] = generate_unique_slug(validated_data["name"], instance=instance)

    for attr, value in validated_data.items():
        setattr(instance, attr, value)

    instance.save()
    return instance
