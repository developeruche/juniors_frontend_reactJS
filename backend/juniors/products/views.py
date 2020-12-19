from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import ProductsSerializer, Products, OrderSerializer
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly, IsAuthenticated
from rest_framework.views import APIView
from user.serializers import CustomUserSerializer
from .models import Orders
from account.authentication import Authentication
# Creating a view for listing all products and single product


class ProductListDetailView(ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly, )


class ProductPageinatorView(ModelViewSet):
    serializer_class = ProductsSerializer
    queryset = Products.objects.all()

    def get_queryset(self):
        data = self.request.query_params.dict()
        skip = data.get("skip", 0)
        amount = data.get("amount", 5)
        page = int(skip) + int(amount)

        return self.queryset[int(skip):page]


class OrderView(APIView):
    serializer_class = CustomUserSerializer
    authentication_classes = (Authentication, )
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        current_user_id = CustomUserSerializer(request.user).data['id']

        # Now get all the orders related to this user
        all_order = Orders.objects.filter(user_id=current_user_id)

        return Response(
            {
                "data": OrderSerializer(all_order, many=True).data
            }
        )
