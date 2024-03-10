from  rest_framework import  serializers
from  .models import Payment

class PaymentSerializer:
    class Base(serializers.ModelSerializer):
        class Meta:
            fields = '__all__'
            model = Payment