from django.urls import path, include

from .views import (
    ProductCreateView,
    ProductRetrieveView,
    ProductListView,
    ProductUpdateDeleteView,
    UserLoginView,
    UserRegistrationView
)

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("register/", UserRegistrationView.as_view(), name="register"),

    path("product/create/", ProductCreateView.as_view(), name="product-create"),
    path("product/list/", ProductListView.as_view(), name="product-list"),
    path("product/<pk>/", ProductRetrieveView.as_view(), name="product-retrieve"),
    path("product/<pk>/update/", ProductUpdateDeleteView.as_view(), name="product-update"),
    path("product/<pk>/delete/", ProductUpdateDeleteView.as_view(), name="product-delete"),
]
