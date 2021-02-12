from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions,viewsets
from .serializers import UserSerializer,PermissionSerializer,RoleSerializer
from .authentication import generate_access_token,JWTAuthentication
from .models import User,Permission,Role

@api_view(['POST'])
def register(request):
    '''User Registration '''
    data = request.data
    if data['password'] != data['password_confirm']:
        raise exceptions.APIException('Password and Confirm Password do not match.')

    serializer = UserSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def login(request):
    '''login view'''
    email = request.data.get('email')
    password = request.data.get('password')
    user = User.objects.filter(email=email).first()

    #checking user
    if user is None:
        raise exceptions.AuthenticationFailed("User Not Found....")

    #checking passwords
    if not user.check_password(password):
        raise exceptions.AuthenticationFailed("incorrect Password..")

    response = Response()
    #generating accaess token
    token = generate_access_token(user)
    response.set_cookie(key='jwt',value=token,httponly=True)
    response.data = {
        'jwt': token
    }

    return response



class AuthenticatedUser(APIView):
    authentication_classes =[JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        serializer = UserSerializer(request.user)
        return Response({
            'data': serializer.data
        })

@api_view(['POST'])
def logout(request):
    '''Logout '''
    response = Response()
    response.delete_cookie(key='jwt')
    response.data = {
        'message': 'success'
    }
    return response


class PermissionAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes= [IsAuthenticated]
    
    def get(self,request):
        serializer = PermissionSerializer(Permission.objects.all(),many=True)
        return Response({
            'data': serializer.data
        })

class RoleViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self,request):
        serializer = RoleSerializer(Role.objects.all(),many=True)
        return Response({
            'data': serializer.data
        })

    def create(self,request):
        pass

    def retrieve(self,request,pk=None):
        pass

    def update(self,request,pk=None):
        pass

    def destroy(self,request,pk=None):
        pass





# @api_view(['GET'])
# def users(request):
#     '''Show all users  '''
#     serializer = UserSerializer(User.objects.all(),many=True)
#     return Response(serializer.data)
