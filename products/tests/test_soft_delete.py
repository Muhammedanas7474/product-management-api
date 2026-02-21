import pytest
from products.services import create_product
from products.models import Product


@pytest.mark.django_db
def test_soft_delete():
    product = create_product(
        name="Delete Me",
        price=200,
        stock=2
    )

    product.is_active = False
    product.save()

    active_products = Product.objects.filter(is_active=True)

    assert product not in active_products
