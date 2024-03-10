import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import mixins, response, status, decorators
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from order.models import Order
from .models import Payment
from django.conf import settings
import stripe
from .serializers import PaymentSerializer


# Create your views here.
class PaymentViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = []


    def get_permissions(self):
        if self.action=='webhook':
            return[]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        try:

            DOMAIN = settings.DOMAIN
            order_id = request.data.get("order_id")
            order = get_object_or_404(Order, id=order_id,user =request.user.id)
            stripe.api_key = settings.STRIPE_SECRET_KEY
            success_url = request.data.get('success_url')
            cancel_url = request.data.get('cancel_url')

            price=stripe.Price.create(
                unit_amount=order.Total,
                currency="usd",
                product_data={"name":f"order No.{order.id}"}
            )
            checkout_session = stripe.checkout.Session.create(

                mode='payment',
                client_reference_id=order.id,
                line_items=[
                    {
                        "price":price.get("id"),
                        "quantity":1,
                    }
                ],
                success_url=DOMAIN + success_url,
                cancel_url=DOMAIN + cancel_url,
            )
            Payment.objects.create(session=checkout_session.get("id"),order=order, status=checkout_session.get("payment_status"))
        except Exception as e:
            return response.Response({"detail": str(e)},status=status.HTTP_404_NOT_FOUND)

        return response.Response({"url": checkout_session.url, }, status=200)

    @csrf_exempt
    @decorators.action(
        detail=False,
        methods=["post"]
    )
    def webhook(self, request, *args, **kwargs):
        endpoint_secret=settings.ENDPOINT_SECRET

        payload = request.body
        event = None

        try:
            event = stripe.Event.construct_from(
              json.loads(payload), stripe.api_key
            )
        except ValueError as e:
            # Invalid payload
            return HttpResponse(status=400)

        # Handle the event

        if event.type == 'checkout.session.completed':
            payment_method = event.data.object # contains a stripe.PaymentMethod
            session_id = event.data.object.id
            payment = get_object_or_404(Payment,session=session_id)
            payment.status='paid'
            payment.save()
        else:
            print('Unhandled event type {}'.format(event.type))

        return HttpResponse(status=200)

