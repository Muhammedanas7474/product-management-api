import pytest
from products.services import create_product, update_product


@pytest.mark.django_db
def test_slug_regenerates_on_name_change():
    product = create_product(
        name="Old Phone",
        price=500,
        stock=5
    )

    old_slug = product.slug

    updated = update_product(product, name="New Phone")

    assert updated.slug != old_slug
