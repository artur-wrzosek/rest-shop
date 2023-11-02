from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework.permissions import BasePermission

from .apps import ShopConfig
from .models import Product, Order

PRODUCT_VIEW_PERMISSION = ("view_product", "Can view product")
PRODUCT_LIST_PERMISSION = ("list_product", "Can view list of products")
PRODUCT_CREATE_PERMISSION = ("create_product", "Can create product")
PRODUCT_UPDATE_PERMISSION = ("update_product", "Can update product")
PRODUCT_DELETE_PERMISSION = ("delete_product", "Can delete product")
ORDER_CREATE_PERMISSION = ("create_order", "Can create order")
STATISTIC_LIST_PERMISSION = ("list_statistic", "Can list statistic")


class PermissionListMixin:
    """
    Mixin for creating a list of permissions based on a given app_name
    and MODELS_PERMISSION dictionary. Argument for a DRF custom BasePermission super() class.
    """
    MODELS_PERMISSIONS = {}
    APP_NAME = ""

    def _build_permissions_list(self) -> list[dict]:
        permission_list = []
        for model, action_list in self.MODELS_PERMISSIONS.items():
            for action in action_list:
                perm = {
                    "codename": f"{action.lower()}_{model.lower()}",
                    "name": f"Can {action.lower()} {model.lower()}",
                    "app_name": f"{self.APP_NAME}",
                    "permission": f"{self.APP_NAME}.{action.lower()}_{model.lower()}"
                }
                permission_list.append(perm)
        return permission_list

    @property
    def permission_list(self) -> list[dict]:
        return self._build_permissions_list()


class BuyerGroupPermissions(BasePermission, PermissionListMixin):
    APP_NAME = ShopConfig.name
    MODELS_PERMISSIONS = {
        "Product": ["view", "list"],
        "Order": ["view", "add", "change"],
    }

    def has_permission(self, request, view):
        user_permissions = request.user.get_all_permissions()
        for perm in self.permission_list:
            if perm["permission"] not in user_permissions:
                return False
        return True


class SellerGroupPermissions(BasePermission, PermissionListMixin):
    APP_NAME = ShopConfig.name
    MODELS_PERMISSIONS = {
        "Product": ["view", "add", "change", "delete", "list"],
        "Order": ["view", "add", "change"],

    }

    def has_permission(self, request, view):
        user_permissions = request.user.get_all_permissions()
        for perm in self.permission_list:
            if perm["permission"] not in user_permissions:
                return False
        return True
