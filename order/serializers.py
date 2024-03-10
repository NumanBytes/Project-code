from rest_framework import serializers
from .models import Order, OrderedItem



class OrderItemSerializer(serializers.ModelSerializer):
    name= serializers.ReadOnlyField(source='product.name')
    class Meta:
        fields = ['name','quantity']
        model = OrderedItem

class OrderSerializer:
    class Base(serializers.ModelSerializer):
        class Meta:
            fields = '__all__'
            model = Order
            # read_only_fields =('user', 'created_at', 'Total', 'arrival_date')

    class Create(serializers.ModelSerializer):

        class Meta:
            fields = '__all__'
            model = Order
            read_only_fields = ('created_at', 'arrival_date')
            write_only_fields=('user',)

    class Retrieve(serializers.ModelSerializer):
        ordered_items = OrderItemSerializer(many=True, read_only=True)

        class Meta:
            model = Order
            fields = ['id', 'Total', 'delivery_address', 'ordered_items']
