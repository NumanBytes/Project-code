from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from . import views

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("", views.OrderViewSet, basename="prders")
urlpatterns = []
urlpatterns += router.urls
