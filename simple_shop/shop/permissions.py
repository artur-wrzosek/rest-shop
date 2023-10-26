from django.db import models
from django.contrib.auth.models import Group
from rest_framework.permissions import BasePermission


BUYERS_PERMISSIONS = (
    ("get_product", "Get product"),
    ("post_product", "Post product"),
    ("update_product", "Update product"),
    ("delete_product", "Delete product"),
)


class BuyersPermissions(BasePermission):
    ACTIONS = {
        "get_product": "buyer.get_product",
        "post_product": "buyer.post_product",
        "update_product": "buyer.update_product",
        "delete_product": "buyer.delete_product",
    }

    def has_permission(self, request, view):
        return self.ACTIONS.get(view.action, "") in request.user.get_all_permissions()

    def has_object_permission(self, request, view, obj):
        return


class BuyersGroup(Group):
    BUYERS = "BUYERS"
    name = models.CharField(max_length=15, default=BUYERS)
    permissions = BuyersPermissions
