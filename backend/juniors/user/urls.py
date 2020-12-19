from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileView, GenericFileuploadView, CategoryListView, ProfilePictureUploadView

router = DefaultRouter(trailing_slash=False)
router.register("profile", UserProfileView)
router.register("file-upload", GenericFileuploadView)
router.register("category-list", CategoryListView)
router.register('profile-pic', ProfilePictureUploadView)

urlpatterns = [
    path("", include(router.urls)),
]
