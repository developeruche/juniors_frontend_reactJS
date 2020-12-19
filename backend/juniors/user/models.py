from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from products.models import GenericFileupload, AddressGlobal, Category, Orders


class CustomUserManager(BaseUserManager):
    # Creating a function for creating the Custom User
    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError("Email Field is required")

        user = self.model(username=username, **extra_fields)
        # the password is not sent to the database as the other fields because django has a special method for hashing password
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, password, **extra_fields):
        # Setting defaul of some fields incase any of it input is not provide
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        # Validating the input to make sure the superuser is alway a staff and superuser
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is staff as True")

        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is staff as True")

        return self._create_user(username, password, **extra_fields)

    def update_password(self, user_id, password):
        if not password:
            raise ValueError(
                "The password Field is required for this operation.")
        user = self.model.objects.get(id=user_id)
        # because we what to update the password and waht the password to be hased also we won't input the passw ord directly but use the provided password hashing manger method(set_password())
        user.set_password(password)
        user.save()


# Creating A custom User

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "username"

    # Introducing a manager which would allow us create superusers
    objects = CustomUserManager()

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    user = models.OneToOneField(
        CustomUser, related_name="user_profile", on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    delivery_addr = models.ForeignKey(
        AddressGlobal, related_name="delivery_address", on_delete=models.CASCADE
    )
    orders = models.ForeignKey(
        Orders, related_name="user_orders", on_delete=models.SET_NULL, null=True, blank=True
    )
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    category = models.ForeignKey(
        Category, related_name="user_product_category", on_delete=models.SET_NULL, null=True
    )
    profile_picture = models.ForeignKey(
        GenericFileupload, related_name="user_image", on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
