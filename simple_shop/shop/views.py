from django.contrib.auth import login, authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
)
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.response import Response

from .permissions import (
    ProductCreatePermissions,
    ProductUpdateDeletePermissions,
    OrderCreatePermissions
)
from .serializers import (
    BaseUserRegistrationSerializer,
    UserLoginSerializer,
    ProductCreateSerializer,
    ProductRetrieveSerializer,
    ProductUpdateDeleteSerializer
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
    permission_classes = (IsAuthenticated, ProductCreatePermissions)
    serializer_class = ProductCreateSerializer


class ProductRetrieveView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductRetrieveSerializer


class ProductListView(ListAPIView):
    permission_classes = (AllowAny,)
    # lookup_field = ['name', 'category', 'description', 'price']


class ProductUpdateDeleteView(DestroyModelMixin, UpdateModelMixin, GenericAPIView):
    permission_classes = (IsAuthenticated, ProductUpdateDeletePermissions)
    serializer_class = ProductUpdateDeleteSerializer
