from rest_framework.permissions import BasePermission

from .apps import ShopConfig


class PermissionListMixin:
    """
    Mixin for creating a list of permissions based on a given app_name
    and MODELS_PERMISSION dictionary. Argument for a DRF custom BasePermission super() class.
    """
    MODELS_PERMISSIONS = {}
    APP_NAME = ""
    PERMISSION_LIST = None

    def _build_permissions_list(self) -> list[dict]:
        permission_list = []
        for model, action_list in self.MODELS_PERMISSIONS.items():
            for action in action_list:
                perm = {
                    "model_name": f"{model}",
                    "codename": f"{action.lower()}_{model.lower()}",
                    "name": f"Can {action.lower()} {model.lower()}",
                    "app_name": f"{self.APP_NAME}",
                    "permission": f"{self.APP_NAME}.{action.lower()}_{model.lower()}"
                }
                permission_list.append(perm)
        return permission_list

    def set_permission_list(self):
        self.PERMISSION_LIST = self._build_permissions_list()


class BuyerGroupPermissions(BasePermission, PermissionListMixin):
    GROUP_NAME = "Buyers"
    APP_NAME = ShopConfig.name
    MODELS_PERMISSIONS = {
        "Product": ["view", "list"],
        "Order": ["view", "add", "change"],
        "Category": ["view", "list"],
    }

    def has_permission(self, request, view):
        user_permissions = request.user.get_all_permissions()
        self.set_permission_list()
        for perm in self.PERMISSION_LIST:
            if perm["permission"] not in user_permissions:
                return False
        return True


class SellerGroupPermissions(BasePermission, PermissionListMixin):
    GROUP_NAME = "Sellers"
    APP_NAME = ShopConfig.name
    MODELS_PERMISSIONS = {
        "Product": ["view", "add", "change", "delete", "list"],
        "Order": ["view", "add", "change"],
        "Category": ["view", "add", "change", "delete", "list"],
    }

    def has_permission(self, request, view):
        user_permissions = request.user.get_all_permissions()
        self.set_permission_list()
        for perm in self.PERMISSION_LIST:
            if perm["permission"] not in user_permissions:
                return False
        return True


class IsOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user
