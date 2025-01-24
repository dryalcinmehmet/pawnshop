

import json

import pytest
from products.models import Product
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User=get_user_model()
######################################################
"""            Product  View Tests.                 """

######################################################
@pytest.mark.django_db
def test_product_list(
    admin_user_obj: User,
    product_obj: Product,
    api_client: APIClient,
):
    """
    Test case for product list
    """
    api_client.force_authenticate(user=admin_user_obj)
    response = api_client.get(reverse("products-viewset-list"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_product_create(
    admin_user_obj: User,
    product_json,
    api_client: APIClient,
):
    """
    Test case for product list
    """
    api_client.force_authenticate(user=admin_user_obj)
    response = api_client.post(reverse("products-viewset-list"), product_json)
    assert response.status_code == 201


@pytest.mark.django_db
def test_product_retrieve(
    admin_user_obj: User,
    product_obj: Product,
    api_client: APIClient,
):
    """Test case for product retrieve"""
    api_client.force_authenticate(user=admin_user_obj)
    response = api_client.get(
        reverse("products-viewset-detail", kwargs={"pk": product_obj.id})
    )

    assert response.status_code == 200
    assert response.data["id"] == str(product_obj.id)
    assert response.data["name"] == str(product_obj.name)
    assert response.data["description"] == str(product_obj.description)
    assert response.data["price"] == str(product_obj.price)
    assert response.data["stock"] == int(product_obj.stock)


@pytest.mark.django_db
def test_product_destroy(
    admin_user_obj: User,
    product_obj: Product,
    api_client: APIClient,
):
    """Test case for product delete"""
    api_client.force_authenticate(user=admin_user_obj)
    assert Product.objects.count() == 1
    response = api_client.delete(
        reverse("products-viewset-detail", kwargs={"pk": product_obj.id})
    )

    assert Product.objects.count() == 0
    assert response.status_code == 200
