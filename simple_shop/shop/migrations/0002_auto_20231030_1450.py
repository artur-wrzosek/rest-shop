from django.contrib.auth.models import Group, Permission
from django.db import migrations
from django.contrib.contenttypes.models import ContentType

from ..models import Product, Order
from ..permissions import (
    PRODUCT_DELETE_PERMISSION,
    PRODUCT_CREATE_PERMISSION,
    PRODUCT_UPDATE_PERMISSION,
    ORDER_CREATE_PERMISSION,
    STATISTICS_VIEW_PERMISSION,
)


roles = {
    "BUYERS": {
        Order: [
            ORDER_CREATE_PERMISSION
        ]
    },
    "SELLERS": {
        Product: [
            PRODUCT_CREATE_PERMISSION,
            PRODUCT_UPDATE_PERMISSION,
            PRODUCT_DELETE_PERMISSION,
            # STATISTICS_VIEW_PERMISSION
        ],
    },
}


def add_group_permissions(apps, schema_editor):
    for role in roles:
        group, group_created = Group.objects.get_or_create(name=role)
        for model, permissions in roles[role].items():
            content_type = ContentType.objects.get_for_model(model)
            for perm in permissions:
                permission, created = Permission.objects.get_or_create(
                    name=perm[1],
                    codename=perm[0],
                    content_type=content_type
                )
                group.permissions.add(permission)
        group.save()


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_group_permissions)
    ]
