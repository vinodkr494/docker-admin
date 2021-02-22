from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions,viewsets,status,generics,mixins
from .serializers import UserSerializer,PermissionSerializer,RoleSerializer
from .authentication import generate_access_token,JWTAuthentication
from .models import User,Permission,Role
from admin.pagination import CustomPagination

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
        data = UserSerializer(request.user).data
        data['permissions'] = [p['name'] for p in data['role']['permissions']]
        return Response({
            'data': data
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
        '''retrive all the role'''
        serializer = RoleSerializer(Role.objects.all(),many=True)
        return Response({
            'data': serializer.data
        })

    def create(self,request):
        '''Creating new role'''
        serializer = RoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'data': serializer.data
        },status=status.HTTP_201_CREATED)

    def retrieve(self,request,pk=None):
        '''retrive role details'''
        role = Role.objects.get(id=pk)
        serializer = RoleSerializer(role)
        
        return Response({
            'data': serializer.data
        })

    def update(self,request,pk=None):
        '''updating the role permission'''
        role = Role.objects.get(id=pk)
        serializer = RoleSerializer(instance=role,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'data': serializer.data
        },status=status.HTTP_202_ACCEPTED)


    def destroy(self,request,pk=None):
        '''Deleting the role'''
        role = Role.objects.get(id=pk)
        role.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserGenericAPIView(
    generics.GenericAPIView,mixins.ListModelMixin,mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,mixins.DestroyModelMixin,mixins.CreateModelMixin
    ):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination

    def get(self,request,pk=None):
        if pk:
            return Response({
                'data': self.retrieve(request,pk).data
                })
        return self.list(request)

    def post(self,request):
        request.data.update({
            'password': 123456,
            'role': request.data['role_id']
        })
        return Response({
            'data': self.create(request).data
        })

    def put(self,request,pk=None):
        if request.data['role_id']:
            request.data.update({
                'role': request.data['role_id']
            })
        return Response({
            'data': self.partial_update(request,pk).data
        })

    def delete(self,request,pk=None):
        return self.destroy(request,pk)


class ProfileInfoAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request ,pk=None):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class ProfilePasswordAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request ,pk=None):
        user = request.user
        if request.data['password'] != request.data['password_confirm']:
            raise exceptions.ValidationError('Passwords do not match')

        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


# @api_view(['GET'])
# def users(request):
#     '''Show all users  '''
#     serializer = UserSerializer(User.objects.all(),many=True)
#     return Response(serializer.data)
