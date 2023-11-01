from rest_framework.permissions import BasePermission


PRODUCT_VIEW_PERMISSION = ("view_product", "Can view product")
PRODUCT_LIST_PERMISSION = ("list_product", "Can view list of products")
PRODUCT_CREATE_PERMISSION = ("create_product", "Can create product")
PRODUCT_UPDATE_PERMISSION = ("update_product", "Can update product")
PRODUCT_DELETE_PERMISSION = ("delete_product", "Can delete product")
ORDER_CREATE_PERMISSION = ("create_order", "Can create order")
STATISTICS_VIEW_PERMISSION = ("view_statistics", "Can view statistics")


class ProductCreatePermissions(BasePermission):
    PERMISSIONS = ["shop.create_product"]

    def has_permission(self, request, view):
        return self.PERMISSIONS in request.user.get_all_permissions()


class ProductUpdateDeletePermissions(BasePermission):
    PERMISSIONS = ["shop.update_product", "shop.delete_product"]

    def has_permission(self, request, view):
        return self.PERMISSIONS in request.user.get_all_permissions()


class OrderCreatePermissions(BasePermission):
    PERMISSIONS = ["shop.create_order"]

    def has_permission(self, request, view):
        return self.PERMISSIONS in request.user.get_all_permissions()


class StatisticsViewPermissions(BasePermission):
    def has_permission(self, request, view):
        return STATISTICS_VIEW_PERMISSION in request.user.get_all_permissions()

