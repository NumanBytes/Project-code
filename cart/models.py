from django.db import models
from django.contrib.auth import get_user_model
from category.models import Product
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

User = get_user_model()


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)

    def __str__(self):
        return f"Cart - {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(_("Quantity"), default=1)

    def clean(self):
        # Check if the cart item's quantity is less than or equal to the product's quantity in inventory
        if self.quantity > self.product.Quantity:
            raise ValidationError('The quantity exceeds the available inventory for this product.')

    @property
    def check_inventory(self):
        if self.quantity > self.product.Quantity:
            return False
        return True

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.product.name} - Quantity: {self.quantity}"
