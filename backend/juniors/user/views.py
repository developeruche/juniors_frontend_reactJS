from account.authentication import Authentication
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile
from .serializers import UserProfileSerializer, AddressGlobalSerializer, GenericFileuploadSerializer, GenericFileupload, AddressGlobal, Category, CategoryListSerializer, CustomUserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from account.authentication import Authentication


class UserProfileView(ModelViewSet):
    queryset = UserProfile.objects.select_related(
        "user", "delivery_addr", "orders", "profile_picture", "category")
    serializer_class = UserProfileSerializer
    authentication_classes = (Authentication, )
    permission_classes = (IsAuthenticated, )

    # Overing the defualt create method
    def create(self, request, *args, **kwargs):
        # First Creating  the Address (It wont be a good user experence if the user have to first create their adress abd come back to create there profile pic and soon on)
        address_serializer = AddressGlobalSerializer(data=request.data)
        address_serializer.is_valid(raise_exception=True)
        address_serializer.save()

        # Now adding the new created address to the request data
        data = {
            **request.data, "delivery_addr_id": address_serializer.data['id']
        }
        # Here i would be validating for full name, email, phonenumber
        email = data.get("email", None)
        phone_number = data.get('phone_number', None)
        full_name = data.get('full_name', None)
        category_value = data.get('category_value', None)
        if not email:
            raise Exception("Email Fields is required.")
        if not full_name:
            raise Exception("You must input fullname.")
        if not phone_number:
            raise Exception("Phone number field is required.")
        if not category_value:
            raise Exception("Category name is required.")

        # here i would search the category table to see if the dent in category is avaliable
        category_value = category_value.capitalize()
        try:
            cat = Category.objects.get(name=category_value)

        except Exception as e:
            raise Exception("The Category Choosen is not avaliable.")

        if cat:
            data = {
                **data, "category_id": cat.id
            }
        else:
            raise Exception("The Category Choosen is not avaliable.")
        try:
            data.pop("category_value")
        except:
            pass
        profile_serializer = self.serializer_class(data=data)
        profile_serializer.is_valid()

        if not profile_serializer.is_valid():
            AddressGlobal.objects.filter(
                id=address_serializer.data['id']).delete()
            raise Exception(profile_serializer.errors)

        profile_serializer.save()

        return Response(
            {
                "sucess": "Profile created."
            },
            status=status.HTTP_201_CREATED
        )

        # Overiding the Update method
    def update(self, request, *args, **kwargs):
        instance = self.get_object()  # This would get the current profile

        data = request.data

        if "address" in data or "city" in data or "state" in data or "country" in data:
            address_instance = self.serializer_class(
                instance).data['delivery_addr']

            address_data = {

            }
            if "address" in data:
                address_data = {
                    **address_data, 'address': data['address'],
                }
            else:
                address_data = {
                    **address_data, 'address': address_instance['address'],
                }

            if "city" in data:
                address_data = {
                    **address_data, 'city': data['city'],
                }
            else:
                address_data = {
                    **address_data, 'address': address_instance['city'],
                }

            if "state" in data:
                address_data = {
                    **address_data, 'state': data['state'],
                }
            else:
                address_data = {
                    **address_data, 'address': address_instance['state'],
                }

            if "country" in data:
                address_data = {
                    **address_data, 'country': data['country'],
                }
            else:
                address_data = {
                    **address_data, 'address': address_instance['country'],
                }

            try:
                # AddressGlobal.objects.filter(
                #     id=address_instance['id']).update(state="Update")
                address_serializer_update = AddressGlobalSerializer(
                    data=address_data
                )
                address_serializer_update.is_valid(raise_exception=True)
                address_serializer_update.save()
                print('reached')
                print(address_serializer_update.data['id'])
                print('passed')

                data = {
                    **data, "delivery_addr_id": address_serializer_update.data['id']
                }

                # deleting the old address to prevent duplicates
                AddressGlobal.objects.filter(
                    id=address_instance['id']).delete()
            except:
                Exception("It didn't work")

        if "category_value" in data:
            # getting the id of the category
            try:
                category_value = data.get("category_value").capitalize()
                cat = Category.objects.get(name=category_value)
            except Exception as e:
                raise Exception("The Category Choosen is not avaliable.")

            if cat:
                data = {
                    **data, "category_id": cat.id
                }

        serializer = self.serializer_class(
            data=data, instance=instance, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        new_object = self.get_object()
        return Response(
            self.serializer_class(new_object).data,
            status=status.HTTP_200_OK
        )


class GenericFileuploadView(ModelViewSet):
    queryset = GenericFileupload.objects.all()
    serializer_class = GenericFileuploadSerializer


class CategoryListView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer


class ProfilePictureUploadView(ModelViewSet):
    queryset = GenericFileupload.objects.all()
    serializer_class = GenericFileuploadSerializer
    authentication_classes = (Authentication, )
    permission_classes = (IsAuthenticated, )

    # overiding the default create method
    def create(self, request, *args, **kwargs):
        data = request.data
        profile_serializer = self.serializer_class(data=data)
        profile_serializer.is_valid(raise_exception=True)
        profile_serializer.save()

        # Now getting the id of the newly saved profile pic so it can be updated in the users profile
        profile_pic_id = profile_serializer.data['id']

        # Now get the profile user at this instance
        current_user_id = CustomUserSerializer(request.user).data['id']

        # Validating
        try:
            vali = UserProfile.objects.get(user_id=current_user_id)
        except:
            raise Exception("Profile not found, create one first.")

        # Now updating the profile
        UserProfile.objects.filter(
            user_id=current_user_id).update(profile_picture_id=profile_pic_id)

        return Response(
            {
                "sucsess": "Profile picture has been setted."
            }
        )
