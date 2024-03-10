from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone
from rest_framework import viewsets, status, decorators
from .serializers import UserSerializer
from utils.enum import UserAccountType
from utils.permissions import IsAdmin, IsGuestUser
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from .models import EmailVerificationToken, ResetPasswordToken
from utils.jwt_email_token import create_token, verify_token

UserModel = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = UserModel.objects.all()
    parser_classes = [MultiPartParser, JSONParser]

    def get_permissions(self):
        if self.action in ['create_buyer', 'verify_email']:
            return [IsGuestUser()]
        elif self.action in ['create_admin']:
            return [IsAdmin()]
        elif self.action in ['me', 'verify_email', 'initiate_verify_email', 'reset_password_email','reset_password']:
            return [IsAuthenticated()]
        else:
            return []

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return self.serializer_class.Update
        else:
            return self.serializer_class.Base

    @decorators.action(
        detail=False,
        methods=["post"]
    )
    def create_buyer(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance: UserModel = serializer.save()
        instance.account_type = UserAccountType.BUYER.value
        instance.set_password(request.data.get("password"))
        instance.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @decorators.action(
        detail=False,
        methods=["post"]
    )
    def create_admin(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance: UserModel = serializer.save()
        instance.account_type = UserAccountType.ADMIN.value
        instance.set_password(request.data.get("password"))
        instance.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @decorators.action(
        detail=False,
        methods=["get", "patch", "delete"]
    )
    def me(self, request, *args, **kwargs):
        if request.method == 'DELETE':
            instance = request.user
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.method == "GET":
            serializer = self.get_serializer(request.user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PATCH':
            serializer = self.get_serializer(request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            instance: UserModel = serializer.save()
            serializer = self.serializer_class.Base(instance)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

    @decorators.action(
        detail=False,
    )
    def initiate_email_verification(self, request, *args, **kwargs):
        if request.user.is_email_verified:
            return Response(data={"message": "Your email is already verified"})
        token_exists = EmailVerificationToken.objects.filter(user=request.user).first()
        new_token = create_token(request.user)
        if token_exists:
            token_exists.token = new_token
            token_exists.save()
        else:
            EmailVerificationToken.objects.create(token=new_token, user=request.user)
        return Response(data={"message": "Please check your email"}, status=status.HTTP_201_CREATED)

    def verify_email(self, request, *args, **kwargs):
        check_token = kwargs.get('token')
        token_exists = EmailVerificationToken.objects.filter(
            Q(token=check_token) & Q(user__is_email_verified=False)).first()
        if token_exists:
            if verify_token(check_token):
                token_exists.user.verify_email()
                token_exists.user.save()
                return Response(data={"message": "Your email is successfully verified"}, status=status.HTTP_200_OK)
            else:
                return Response(data={"message": "The token is expired."})
        else:
            return Response(data={"message": "The token is invalid or the email is already verified"},
                            status=status.HTTP_200_OK)

    @decorators.action(
        detail=False,
    )
    def reset_password_email(self, request, *args, **kwargs):
        user = request.user
        response = user.reset_password
        if response:
            return Response(data={"message": "Reset password email has been sent"}, status=status.HTTP_200_OK)
        return Response(data={"message": "Reset password email couldn't be sent"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @decorators.action(
        detail=False,
        methods=["POST"],
        name="custom"
    )
    def reset_password(self, request, *args, **kwargs):
        token = request.query_params.get('token')
        token_exists = ResetPasswordToken.objects.filter(token=token).first()
        if not token_exists:
            return Response(data={"message": "Token is invalid"})
        elif token_exists.expiry < timezone.now():
            return Response(data={"message": "The token is expired Please generate a new one."},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            new_password = request.data.get('password')
            confirm_password = request.data.get('confirm_password')
            if new_password == confirm_password:
                user = get_user_model().objects.filter(id=request.user.id).first()
                user.set_password(new_password)
                user.save()
                token_exists.delete()
                return Response({"message": "Your password has been updated"}, status=status.HTTP_200_OK)
