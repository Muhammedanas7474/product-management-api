import pytest
from products.services import create_product
from products.models import Product


@pytest.mark.django_db
def test_slug_uniqueness():
    product1 = create_product(
        name="iPhone",
        price=1000,
        stock=10
    )

    product2 = create_product(
        name="iPhone",
        price=1200,
        stock=5
    )

    assert product1.slug != product2.slug
