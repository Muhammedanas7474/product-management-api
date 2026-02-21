import os
from io import BytesIO

from celery import shared_task
from django.conf import settings
from django.core.files.base import ContentFile
from PIL import Image

from .models import Product


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
)
def generate_thumbnail(self, product_id):
    product = Product.objects.get(id=product_id)

    # Idempotency check
    if product.thumbnail:
        return "Thumbnail already exists"

    if not product.image:
        return "No image to process"

    image = Image.open(product.image.path)

    size = settings.THUMBNAIL_SIZE
    quality = settings.THUMBNAIL_QUALITY

    image.thumbnail((size, size))

    thumb_io = BytesIO()
    image.save(thumb_io, format="JPEG", quality=quality)

    thumb_name = f"thumb_{os.path.basename(product.image.name)}"

    product.thumbnail.save(
        thumb_name,
        ContentFile(thumb_io.getvalue()),
        save=True,
    )

    return "Thumbnail generated"
