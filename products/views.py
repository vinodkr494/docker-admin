from rest_framework import generics,mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.authentication import JWTAuthentication
from .models import Product
from .serializers import ProductSerializer
from admin.pagination import CustomPagination

class ProductGenericAPIView(
    generics.GenericAPIView,mixins.ListModelMixin,mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,mixins.DestroyModelMixin,mixins.CreateModelMixin
    ):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPagination

    def get(self,request,pk=None):
        if pk:
            return Response({
                'data': self.retrieve(request,pk).data
                })
        return self.list(request)

    def post(self,request):
       
        return Response({
            'data': self.create(request).data
        })

    def put(self,request,pk=None):
       
        return Response({
            'data': self.partial_update(request,pk).data
        })

    def delete(self,request,pk=None):
        return self.destroy(request,pk)
