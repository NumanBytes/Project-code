from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Category


class ProductSerializer:
    class Create(serializers.ModelSerializer):
        class Meta:
            fields = ['name', 'description', 'Price', 'Quantity', 'Category'
                , 'image', 'imageURL']
            model = Product
    class Base(serializers.ModelSerializer):
        Category = CategorySerializer()

        class Meta:
            fields = ['id','name', 'description', 'Price', 'Quantity', 'image', 'imageURL', 'Category']
            model = Product