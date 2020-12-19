import jwt
from .models import Jwt
from user.models import CustomUser
from datetime import datetime, timedelta
from django.conf import settings
import random
import string
from rest_framework.views import APIView
from .serializers import LoginSerializer, RegisterSerializer, RefreshSerializer, ResetPasswordSerializer
from django.contrib.auth import authenticate
from rest_framework.response import Response
from .authentication import Authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.core.signing import TimestampSigner
from decouple import config

# This fuction would return a random string that the refresh token would carry as data


def create_rand_string(length):
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))


def get_access_token(payload):
    expiration_time = datetime.now() + timedelta(minutes=7)
    return jwt.encode(
        {"exp": expiration_time.timestamp(), **payload},
        settings.SECRET_KEY,
        algorithm="HS256"
    )


def get_refresh_token():
    expiration_time = datetime.now() + timedelta(minutes=7)
    return jwt.encode(
        {"exp": expiration_time.timestamp(),
         "data": create_rand_string(10)},
        settings.SECRET_KEY,
        algorithm="HS256"
    )


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        # Validateing data
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # that authenticate method is responsible for comparing email and hashed password
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'])

        if not user:
            return Response(
                {
                    "error": "Invaild username or Password"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Deleting any occurance of the currently logined user id (This would ensure there are no duplicates)
        Jwt.objects.filter(user_id=user.id).delete()

        # Creating access token
        access = get_access_token({
            "user_id": user.id
        })

        # Creating refresh token
        refresh = get_refresh_token()

        # Storing access token refresh token and user
        Jwt.objects.create(
            user_id=user.id,
            access=access.decode(),
            refresh=refresh.decode()
        )

        return Response(
            {
                "resError": False,
                "access": access,
                "refresh": refresh
            },
            status=status.HTTP_200_OK
        )


class RegisterView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        # validating the sent in data
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # creating the user
        CustomUser.objects._create_user(**serializer.validated_data)

        return Response(
            {
                "resError": False,
                "success": "User Created"
            },
            status=status.HTTP_201_CREATED
        )


# Which the end point the frontend enginner would send the current refresh to this route
# if the token is valid this route would return a new access token and refresh token

class RefreshView(APIView):
    serializer_class = RefreshSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            active_jwt = Jwt.objects.get(
                refresh=serializer.validated_data['refresh'])
        except Exception as e:
            raise Exception("JWT token cannot be found.")

        # Validating refresh Token
        if not Authentication.verify_jwt_token(serializer.validated_data['refresh']):
            raise Exception("Token has expired or tampered with.")

        access = get_access_token({
            "user_id": active_jwt.user.id
        })
        refresh = get_refresh_token()

        # Here the newly created access token and refresh token are stored in the database
        active_jwt.access = access.decode()
        active_jwt.refresh = refresh.decode()
        active_jwt.save()

        # access token and refresh token is return for frontend comsuption
        return Response(
            {
                "resError": False,
                "access": access,
                "refresh": refresh
            }
        )


class PreRestPassword(APIView):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Creating the new unique url and encrypting a data that would be used for vaildation
        appname = "DemoJuniorsStore"
        data = f"{appname}_{str(request.user)}"
        signer = TimestampSigner(salt=config("_APP_SALT_"))
        signed_data = signer.sign(data)
        new_url = str(signed_data).split(":")
        new_url = new_url[1]+":"+new_url[2]

        return Response(
            {
                "resError": False,
                "reset-url": new_url
            }
        )


class ResetPassword(APIView):
    serializer_class = ResetPasswordSerializer
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        reset_url = kwargs.get("reset_url", None)
        if not reset_url:
            raise Exception("You are missing the reset url.")

        # Here i would decrypt my encryption to vaildate the incoming url
        appname = "DemoJuniorsStore"
        data = f"{appname}_{str(request.user)}"
        signer = TimestampSigner(salt=config("_APP_SALT_"))
        d_formatted_data = formatted_data = f"{data}:{reset_url}"
        print(d_formatted_data)
        try:
            signer.unsign(formatted_data, max_age=180)
        except Exception:
            raise Exception("Expired or invalided reset URL.")

        # Now all neccesary validation have been done it time to update password
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = CustomUser.objects.update_password(
            user_id=request.user.id, **serializer.validated_data)
        x = datetime.now() + timedelta(minutes=1)
        return Response(
            {
                "success": "Password changed Successfully."
            }
        )
