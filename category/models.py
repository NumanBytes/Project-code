from uuid import uuid4
from django.db import models
from django.utils.translation import gettext_lazy as _


def product_photo_upload(instance, filename):
    ext = filename.split('.')[-1]
    prefix = uuid4().hex
    filename_ = prefix + '.' + ext
    return f"product/{filename_}"


# Create your models here.
class Category(models.Model):
    name = models.CharField(_("Category Name"), max_length=150, null=False, blank=False, unique=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
    def __str__(self):
        return f"{self.id} - {self.name}"


class Product(models.Model):
    name = models.CharField(_("Product Name"), max_length=150, null=False, blank=False, unique=True)
    description = models.CharField(_("Product Description"), max_length=150, null=False, blank=False)
    Price = models.IntegerField(_("Price of Product"), null=False, blank=False)
    Quantity = models.IntegerField(_("Quantity of Product"), null=False, blank=False)
    Category = models.ForeignKey("Category", on_delete=models.CASCADE, verbose_name=_("Category of Product"),
                                 null=False, blank=False)
    image = models.ImageField(_("Product Image"), blank=True, null=True, upload_to=product_photo_upload, max_length=255)
    imageURL = models.URLField(verbose_name="Image url", blank=True, null=True)


    def __str__(self):
        return f"{self.id} - {self.name}"
