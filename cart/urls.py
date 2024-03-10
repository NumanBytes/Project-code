from django.conf import settings
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, )
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_simplejwt.views import TokenBlacklistView,TokenVerifyView
from django.urls import path
from . import views

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("", views.CartItemViewSet, basename="cart")

urlpatterns = []

urlpatterns += router.urls
