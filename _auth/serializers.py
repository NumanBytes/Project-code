from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import EmailVerificationToken

UserModel = get_user_model()


class UserSerializer:
    class Base(serializers.ModelSerializer):
        class Meta:
            fields = ['id', 'full_name', 'image', 'email', 'username', 'phone_number', 'password', 'account_type',
                      'badges']
            model = UserModel
            search_fields = ['email']
            read_only_fields = ['account_type', 'badges']
            extra_kwargs = {
                'password': {'write_only': True}
            }

    class Update(Base):
        class Meta:
            fields = ['id', 'full_name', 'image', 'phone_number']
            model = UserModel


class EmailVerificationTokenSerializer(serializers.Serializer):
    class Meta:
        fields = ['__all__']
        model = EmailVerificationToken
        read_only_fields=['token']
