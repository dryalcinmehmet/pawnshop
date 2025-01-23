from products.models import Product
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    price = serializers.DecimalField(max_digits=5,decimal_places=1)
    stock = serializers.IntegerField(required=True)


    def validate(self, data):
        """
        Check that data.
        """
        if not data:
            raise ValidationError({})
        return data

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "stock",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "name",
            "description",
            "price",
            "stock",
            "created_at",
            "updated_at",
        ]



class ProductDeleteSerializer(serializers.ModelSerializer):


    def validate(self, data):
        """
        Check that data.
        """
        if not data:
            raise ValidationError({})
        return data

    class Meta:
        model = Product
        fields = [
            "id",
        ]



class ProductListOrDetailSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    price = serializers.DecimalField(max_digits=5,decimal_places=1)
    stock = serializers.IntegerField(required=True)


    def validate(self, data):
        """
        Check that data.
        """
        if not data:
            raise ValidationError({})
        return data

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "stock",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "name",
            "description",
            "price",
            "stock",
            "created_at",
            "updated_at",
        ]


class ProductCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    price = serializers.DecimalField(max_digits=5,decimal_places=1)
    stock = serializers.IntegerField(required=True)


    def validate(self, data):
        """
        Check that data.
        """
        if not data:
            raise ValidationError({})
        return data

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "stock",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

class ProductUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    price = serializers.DecimalField(max_digits=5,decimal_places=1)
    stock = serializers.IntegerField(required=True)


    def validate(self, data):
        """
        Check that data.
        """
        if not data:
            raise ValidationError({})
        return data

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "stock",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]
