from rest_framework import serializers
from .models import Cart, CartItem
from django.utils.translation import gettext_lazy as _
from category.serializers import ProductSerializer


class CartItemSerializer:
    class Base(serializers.ModelSerializer):
        class Meta:
            model = CartItem
            fields = ['id', 'cart', 'product', 'quantity']
            validators = [
                serializers.UniqueTogetherValidator(
                    queryset=model.objects.all(),
                    fields=('cart', 'product'),
                    message=_("Product already exists in cart.")
                )
            ]

        def validate(self, attrs):
            product = attrs.get('product')
            quantity = attrs.get('quantity')

            if quantity > product.Quantity:
                raise serializers.ValidationError("Quantity exceeds available products in inventory")
            return attrs

    class List(serializers.ModelSerializer):
        product = ProductSerializer.Base()

        class Meta:
            model = CartItem
            fields = ['id', 'cart', 'product', 'quantity']
            validators = [
                serializers.UniqueTogetherValidator(
                    queryset=model.objects.all(),
                    fields=('cart', 'product'),
                    message=_("Product already exists in cart.")
                )
            ]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer.Base(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'items']
