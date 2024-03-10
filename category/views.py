from rest_framework import viewsets
from .serializers import CategorySerializer, ProductSerializer
from .models import Category, Product
from utils.permissions import IsAdmin, IsGuestUser
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework import viewsets, status, decorators,response
from rest_framework.permissions import SAFE_METHODS


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = []

    def get_permissions(self):
        if not self.request.method in SAFE_METHODS:
            return [IsAdmin()]
        return []


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = []
    parser_classes = [MultiPartParser, JSONParser]

    def get_permissions(self):
        if not self.request.method in SAFE_METHODS:
            return [IsAdmin()]
        return []

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return self.serializer_class.Base
        return self.serializer_class.Create

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        serializer_ = self.serializer_class.Base(serializer.instance)

        return response.Response(serializer_.data, status=status.HTTP_201_CREATED, headers=headers)