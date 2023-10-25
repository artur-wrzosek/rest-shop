from django.db import models
from django.contrib.auth.models import User


class BaseUser(User):
    BUYER = "BUYER"
    SELLER = "SELLER"
    ROLE_CHOICES = (
        (BUYER, "Buyer"),
        (SELLER, "Seller"),
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES)


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Category(models.Model):
    name = models.CharField(max_length=50)


class Product(BaseModel):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=200, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(to=Category, on_delete=models.SET_NULL)
    photo_url = models.ImageField()
    photo_mini_url = models.ImageField()


class OrderItem(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    summary_price = models.DecimalField(max_digits=6, decimal_places=2)


class OrderList(BaseModel):
    item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    final_price = models.DecimalField(max_digits=6, decimal_places=2)


class Order(BaseModel):
    client = models.ForeignKey(to=BaseUser, on_delete=models.DO_NOTHING)
    address = models.CharField(max_length=100)
    order_list = models.OneToOneField(to=OrderList, on_delete=models.CASCADE)
    payment_date = models.DateField()
