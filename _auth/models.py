import secrets
import uuid
from datetime import timedelta
from uuid import uuid4

from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from utils.enum import UserAccountType
from utils.email_client import EmailClient

# Create your models here.

email_sender = EmailClient()


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("account_type", UserAccountType.ADMIN.value)
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)


def image_upload(instance, filename):
    ext = filename.split('.')[-1]
    prefix = uuid4().hex
    filename_ = prefix + '.' + ext
    return f"profile/{filename_}"


class User(AbstractUser):
    full_name = models.CharField(
        _("Full Name"), null=False, blank=False, max_length=255
    )
    email = models.EmailField(
        _("Email"), null=False, blank=False, max_length=225, unique=True
    )
    username = models.CharField(
        _("Username"), null=True, blank=True, max_length=225, unique=True
    )
    is_email_verified = models.BooleanField(
        _("Email Verified?"), default=False, blank=True, null=False
    )
    phone_number = models.CharField(
        _("Phone Number"), max_length=50, null=True, blank=True, unique=False
    )
    account_type = models.CharField(
        _("Account Type"), null=False, blank=False, max_length=32, editable=False, choices=UserAccountType.choices()
    )
    image = models.ImageField(_("Profile Photo"), blank=True, null=True, upload_to=image_upload, max_length=255)
    badges = models.PositiveIntegerField(_("User Badges"), null=False, blank=False, default=0)

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    objects = UserManager()

    def verify_email(self):
        self.is_email_verified = True

    def save(self, *args, **kwargs):
        # is_new = self.pk is None
        # if is_new:
        #     email_sent = email_sender.send_signup_email(user=self)
        #     if not email_sent:
        #         print("The email was not sent")
        response = super().save(*args, **kwargs)
        return response

    @property
    def reset_password(self, *args, **kwargs):
        token = self.create_reset_token()
        email_sent = email_sender.reset_password_email(user=self, token=token)
        if not email_sent:
            print("email was not sent")
            response = False
        response = True
        return response

    def create_reset_token(self):
        token = secrets.token_hex(nbytes=16)
        Token = ResetPasswordToken.objects.create(token=token, user=self)
        Token.save()
        return token

    def __str__(self):
        return f"User - {self.id} - {self.full_name or ''}"

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class EmailVerificationToken(models.Model):
    token = models.CharField(_("Email Verify Token"), max_length=150, null=False, blank=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.token}"


def expiration():
    return timezone.now() + timedelta(days=1)


class ResetPasswordToken(models.Model):
    token = models.CharField(_("Email Verify Token"), max_length=150, null=False, blank=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expiry = models.DateTimeField(max_length=150, null=False, blank=False, default=expiration())

    def __str__(self):
        return f"{self.token}"
