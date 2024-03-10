from django.http import QueryDict
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .serializers import CartSerializer, CartItemSerializer
from .models import CartItem, Cart
from rest_framework.response import Response


# Create your views here.
class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer.Base
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CartItemSerializer.List
        return CartItemSerializer.Base

    def get_queryset(self):
        cart_, _ = Cart.objects.get_or_create(user=self.request.user)
        return self.queryset.filter(cart=cart_.id)

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, QueryDict):  # optional
            request.data._mutable = True
        cart_, _ = Cart.objects.get_or_create(user=self.request.user)
        request.data['cart'] = cart_.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
