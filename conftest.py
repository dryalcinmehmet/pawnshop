import os
import subprocess
from datetime import datetime

import pytest
from django.apps import apps
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()
Product = apps.get_model("products", "Product")


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def admin_user_obj():
    user_obj = User.objects.create_user(
        username="admin",
        email="admin_user@aractakasi.com",
        password="admin",
        first_name="Admin",
        last_name="Admin",
        is_active=True,
        is_staff=True,
        is_superuser=True,
    )
    return user_obj


@pytest.mark.django_db()
def create_product(
    name: str,
    description: str,
    price: str,
    stock: int,
) -> Product:
    model = Product.objects.create(
        name=name, description=description, price=price, stock=stock
    )
    return model


@pytest.fixture
def product_obj(
    name: str = "The Davinci code",
    description: str = "by Dan Brown",
    price: str = "13.2",
    stock: int = 10,
) -> Product:
    return create_product(name=name, description=description, price=price, stock=stock)


@pytest.fixture
def product_json(product_obj: Product):
    return {
        "name": "The Davinci code",
        "description": "by Dan Brown",
        "price": "13.2",
        "stock": 10,
    }
