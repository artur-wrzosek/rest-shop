from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from rest_framework import serializers

from .models import BaseUser, Product, Category


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100, write_only=True)

    def validate(self, attrs):
        username = attrs.get("username", None)
        password = attrs.get("password", None)
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Wrong username or password")
        else:
            raise serializers.ValidationError("Username and password required")
        attrs["user"] = user
        return attrs


class BaseUserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = "__all__"

    def create(self, validated_data):
        user = BaseUser.objects.create_user(**validated_data)
        groups_ids = Group.objects.filter(name__contains=user.role).values_list(flat=True)
        user.groups.set(groups_ids)
        user.save()
        return user


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductCreateSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = "__all__"

    def create(self, validated_data):
        category = validated_data.pop("category", None)
        if category:
            category, created = Category.objects.get_or_create(name=category)
        product = Product.objects.create(category=category, **validated_data)
        return product


class ProductRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id"]


class ProductUpdateDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id"]
