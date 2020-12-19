from rest_framework import serializers
from .models import GenericFileupload, Orders, AddressGlobal, Products


class GenericFileuploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = GenericFileupload
        fields = "__all__"


class ProductsSerializer(serializers.ModelSerializer):

    product_image = GenericFileuploadSerializer(read_only=True)
    product_image_id = serializers.IntegerField(write_only=True)
    category = serializers.SerializerMethodField("get_category_data")
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Products
        fields = "__all__"

    def get_category_data(self, obj):
        from user.serializers import CategoryListSerializer
        return CategoryListSerializer(obj.category).data


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField("get_user_data")
    user_id = serializers.IntegerField(write_only=True)
    products = ProductsSerializer(read_only=True)
    products_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Orders
        fields = "__all__"

    def get_user_data(self, obj):
        from user.serializers import CustomUserSerializer
        return CustomUserSerializer(obj.user).data


class AddressGlobalSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressGlobal
        fields = "__all__"
