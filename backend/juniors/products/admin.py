from django.contrib import admin
from .models import GenericFileupload, AddressGlobal, Category, Products, Orders

admin.site.register((GenericFileupload, AddressGlobal,
                     Category, Products, Orders, ))
