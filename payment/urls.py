from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from . import views

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("", views.PaymentViewSet, basename="category")

urlpatterns = []
urlpatterns += router.urls
