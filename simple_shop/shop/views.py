from django.contrib.auth import login
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView,
)
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.response import Response

from django_filters import rest_framework as filters

from .models import Product
from .permissions import BuyerGroupPermissions, SellerGroupPermissions, IsOwnerPermission

from .serializers import (
    BaseUserRegistrationSerializer,
    UserLoginSerializer,
    ProductCreateSerializer,
    ProductRetrieveSerializer,
    OrderCreateSerializer,
    ProductUpdateSerializer,
    ProductDeleteSerializer,
    ProductListRetrieveSerializer,
)


class UserLoginView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request=request, user=user)
        return Response(status=status.HTTP_202_ACCEPTED)


class UserRegistrationView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = BaseUserRegistrationSerializer


class ProductCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated, SellerGroupPermissions)
    serializer_class = ProductCreateSerializer


class ProductUpdateView(UpdateAPIView):
    permission_classes = (IsAuthenticated, SellerGroupPermissions, IsOwnerPermission)
    serializer_class = ProductUpdateSerializer
    queryset = Product.objects.all()


class ProductDeleteView(DestroyAPIView):
    permission_classes = (IsAuthenticated, SellerGroupPermissions, IsOwnerPermission)
    serializer_class = ProductDeleteSerializer
    queryset = Product.objects.all()


class ProductRetrieveView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductRetrieveSerializer
    queryset = Product.objects.all()


class ProductListRetrieveView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductListRetrieveSerializer
    filter_backends = [filters.DjangoFilterBackend]
    pagination_class = PageNumberPagination

    # TODO: changing filters to corresponding filterset
    def _get_filters(self):
        filters_dict = {}
        if name := self.request.query_params.get("name", None):
            filters_dict["name__icontains"] = name
        if category := self.request.query_params.get("category", None):
            filters_dict["category__name__icontains"] = category
        if description := self.request.query_params.get("description", None):
            filters_dict.update({"description__icontains": phrase for phrase in description.split()})
        if price := self.request.query_params.get("price", None):
            filters_dict["price__exact"] = price
        if price_min := self.request.query_params.get("price_min", None):
            filters_dict["price__gte"] = price_min
        if price_max := self.request.query_params.get("price_max", None):
            filters_dict["price__lte"] = price_max
        return filters_dict

    def get_queryset(self):
        return Product.objects.filter(**self._get_filters())


class StatisticProductListView(ListAPIView):
    permission_classes = (IsAuthenticated, SellerGroupPermissions)
    queryset = Product.objects.all()


class OrderCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated, SellerGroupPermissions | BuyerGroupPermissions)
    serializer_class = OrderCreateSerializer
