from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductListDetailView, ProductPageinatorView, OrderView


router = DefaultRouter()
router.register("products", ProductListDetailView)
router.register("page-control", ProductPageinatorView)

urlpatterns = [
    path("", include(router.urls)),
    path("orders", OrderView.as_view())
]
