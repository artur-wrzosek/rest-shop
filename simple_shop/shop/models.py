from django.db import models
from django.contrib.auth.models import AbstractUser


class BaseUser(AbstractUser):
    BUYER = "BUYER"
    SELLER = "SELLER"
    ROLE_CHOICES = (
        (BUYER, "Buyer"),
        (SELLER, "Seller"),
    )

    role = models.CharField(max_length=15, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.role}: {self.username}"


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(to=BaseUser, on_delete=models.SET_NULL, null=True)

    objects = models.Manager()

    class Meta:
        abstract = True


class Category(BaseModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


class Product(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=200, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(to=Category, related_name="products", on_delete=models.SET_NULL, null=True)
    photo_url = models.ImageField(upload_to="photos/", blank=True, null=True)
    photo_mini_url = models.ImageField(upload_to="photos/", width_field=200, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class OrderItem(BaseModel):
    product = models.ForeignKey(to=Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    summary_price = models.DecimalField(max_digits=6, decimal_places=2)
    order = models.ForeignKey("Order", related_name="order_items", on_delete=models.CASCADE)


class Order(BaseModel):
    buyer_address = models.CharField(max_length=100)
    final_price = models.DecimalField(max_digits=6, decimal_places=2)
    payment_date = models.DateField()
    is_paid = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)
