import datetime
from django.conf import settings
import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.contrib.auth import get_user_model


def generate_access_token(user):
    payload ={
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'iat': datetime.datetime.utcnow()
    }

    return jwt.encode(payload,settings.SECRET_KEY,algorithm='HS256')

class JWTAuthentication(BaseAuthentication):
    
    def authenticate(self,request):
        token = request.COOKIES.get('jwt')

        if not token:
            return None

        try :

            payload = jwt.decode(token,settings.SECRET_KEY,algorithms='HS256')

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('unauthenticated')

        user = get_user_model().objects.filter(id=payload['user_id']).first()

        if user is None:
            raise exceptions.AuthenticationFailed('user not found')

        return (user,None)



