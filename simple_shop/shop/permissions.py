from django.db import models
from django.contrib.auth.models import Group


class BuyersGroup(Group):
    BUYERS = "BUYERS"
    GROUP_NAME = (BUYERS, "Buyers")
    name = models.CharField(max_length=15, choices=GROUP_NAME)
