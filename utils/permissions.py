from rest_framework.permissions import BasePermission
from .enum import UserAccountType as UAT

class IsGuestUser(BasePermission):
    """
    Allows access only to non-authenticated users.
    """

    def has_permission(self, request, view):
        return not request.user.is_authenticated

class IsAdmin(BasePermission):
    """
    Allows access only to non-authenticated users.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.account_type == UAT.ADMIN.value
        return False

class IsBuyer(BasePermission):
    """
    Allows access only to non-authenticated users.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.account_type == UAT.BUYER.value
        return False
