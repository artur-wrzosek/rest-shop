from django.urls import path, include

from .views import (
    ProductCreateView,
    ProductRetrieveView,
    ProductListRetrieveView,
    ProductDeleteView,
    ProductUpdateView,
    UserLoginView,
    UserRegistrationView
)

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("register/", UserRegistrationView.as_view(), name="register"),

    path("product/", ProductListRetrieveView.as_view(), name="product-list"),
    path("product/create/", ProductCreateView.as_view(), name="product-create"),
    path("product/<int:pk>/", ProductRetrieveView.as_view(), name="product-retrieve"),
    path("product/<int:pk>/update/", ProductUpdateView.as_view(), name="product-update"),
    path("product/<int:pk>/delete/", ProductDeleteView.as_view(), name="product-delete"),
]
