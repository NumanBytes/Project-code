from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from django.db import transaction

from .models import Order, OrderedItem
from rest_framework import mixins, viewsets, status, decorators
from .serializers import OrderSerializer, OrderItemSerializer
from rest_framework.response import Response
from cart.models import Cart, CartItem


# TODO
# ORDER PLACE KRNA USER K OR QUANTITY KO VALIDATE KRNA HA STH KNSA VIEW USE KRNA H

class OrderViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        instance =self.get_queryset()
        serializer = self.serializer_class.Retrieve(instance,many=True)
        return Response(serializer.data)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        cart_, _ = Cart.objects.get_or_create(user=self.request.user)
        cart_items = CartItem.objects.filter(cart=cart_.id)
        if not cart_items:
            return Response({"detail": "Cart is empty. Cannot place an order with an empty cart."},
                            status=status.HTTP_400_BAD_REQUEST)
        address = request.data.get('delivery_address')
        total_amount = sum(item.product.Price * item.quantity for item in cart_items)

        for cart_item in cart_items:
            if not cart_item.check_inventory:
                return Response({
                    "detail": f"The quantity of {cart_item.product.name} exceeds the available inventory. Limit is {cart_item.product.Quantity} and you ordered {cart_item.quantity}"},
                    status=status.HTTP_400_BAD_REQUEST)
        order = {"user": request.user.id, "Total": total_amount, "delivery_address": address}
        order_serializer = self.serializer_class.Create(data=order)
        order_serializer.is_valid(raise_exception=True)
        order = order_serializer.save()
        ordered_item_list = []
        for cart_item in cart_items:
            obj = OrderedItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity
            )
            obj.update_product_quantity
            serializer = OrderItemSerializer(obj)
            ordered_item_list.append(serializer.data)
        cart_.delete()
        response_ = {"messagre": "Your order has been placed successfully", "order": order_serializer.data,
                     "items": ordered_item_list}

        return Response(response_, status=status.HTTP_201_CREATED)
