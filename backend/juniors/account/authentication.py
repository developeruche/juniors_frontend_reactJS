import jwt
from django.conf import settings
from datetime import datetime
from rest_framework.authentication import BaseAuthentication
from user.models import CustomUser


class Authentication(BaseAuthentication):
    # Overiding the authenitcate method
    def authenticate(self, request):
        # validating the headers
        data = self.validate_request(request.headers)
        if not data:
            # return the user as none and is_authenticated as none
            return None, None

        return self.get_user(data["user_id"]), None
        # return print(data), None

    def get_user(self, user_id):
        try:
            user = CustomUser.objects.get(id=user_id)
            return user
        except Exception:
            return None

    def validate_request(self, headers):
        authorization = headers.get('Authorization', None)
        if not authorization:
            return None
        token = authorization[7:]
        decoded_token = Authentication.verify_jwt_token(token)
        if not decoded_token:
            return None

        return decoded_token

    @staticmethod
    def verify_jwt_token(token):
        # Decoding the token
        try:
            d = jwt.decode(token, settings.SECRET_KEY, algorithm="HS256")
        except Exception:
            return None

        # Validate to see if token is Expired
        exp = d['exp']

        if datetime.now().timestamp() > exp:
            return None

        return d
