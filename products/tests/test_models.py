import pytest
from products.models import Product


# Address model test.
@pytest.mark.django_db
def test_create_product(product_obj: Product):
    assert Product.objects.filter(id=product_obj.id).exists()
    assert product_obj.__str__() == product_obj.name
