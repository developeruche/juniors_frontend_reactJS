from products.serializers import GenericFileuploadSerializer, OrderSerializer, GenericFileupload, AddressGlobalSerializer
from rest_framework import serializers
from .models import UserProfile, CustomUser, AddressGlobal, Category


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"


class UserProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    delivery_addr = AddressGlobalSerializer(read_only=True)
    delivery_addr_id = serializers.IntegerField(write_only=True)
    orders = OrderSerializer(read_only=True)
    profile_picture = GenericFileuploadSerializer(read_only=True)
    profile_picture_id = serializers.IntegerField(
        write_only=True, required=False)
    category = CategoryListSerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    category_value = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = UserProfile
        fields = "__all__"
