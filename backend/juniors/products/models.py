from django.db import models


class GenericFileupload(models.Model):
    file_upload = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_upload}"


class AddressGlobal(models.Model):
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.address


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    product_image = models.ForeignKey(
        GenericFileupload, related_name="product_image", on_delete=models.SET_NULL, null=True
    )
    price = models.IntegerField()
    time_it_takes_for_delivery = models.TextField()
    category = models.ForeignKey(
        Category, related_name="product_category", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Orders(models.Model):
    user = models.ForeignKey(
        "user.CustomUser", related_name="order_user", on_delete=models.CASCADE
    )
    products = models.ForeignKey(
        Products, related_name="order_product", on_delete=models.CASCADE
    )
    is_delivered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} -|- {str(self.is_delivered)}"

    # class Meta:
    #     order_by =
