from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from category.models import Product
from django.utils import timezone

User = get_user_model()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    Total = models.PositiveIntegerField(_("Quantity"), default=1)
    delivery_address = models.CharField(_("Delivery Address"), max_length=150,blank=False, null=False )
    arrival_date = models.DateTimeField(_("Estimated Arrival Date"), blank=False, null=False,
                                        default=timezone.now() + timezone.timedelta(days=7))

    def __str__(self):
        return f"{self.id} - {self.user}"


class OrderedItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='ordered_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(_("Quantity Ordered"), default=1)

    def __str__(self):
        return f"{self.id} - {self.product}"
    @property
    def update_product_quantity(self):
        self.product.Quantity -= self.quantity
        self.product.save()
    @property
    def restore_product_inventory(self):
        self.product.Quantity += self.quantity
        self.product.save()
