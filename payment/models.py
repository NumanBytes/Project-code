from django.db import models
from django.utils.translation import gettext_lazy as _
from order.models import Order


class Payment(models.Model):
    order = models.OneToOneField("order.Order", blank=False, null=True, on_delete=models.SET_NULL)
    session = models.CharField(max_length=255, null=False, blank=False)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    status = models.CharField(_("Payment status"), max_length=255)

    def __str__(self):
        return f"{self.id} - {self.session}"
