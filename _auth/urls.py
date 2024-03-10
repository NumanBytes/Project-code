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

router.register("", views.UserViewSet, basename="auth")

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('verify_email/<str:token>/',views.UserViewSet.as_view({'get':'verify_email'}),name='auth_verify_email')]

urlpatterns += router.urls
