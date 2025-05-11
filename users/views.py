from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .custom_permissions import IsSuperUser
from .serializers import RegistrationSerializer,LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import status
from config import settings

def get_token_for_user(user):
    refresh_token = RefreshToken.for_user(user)
    return {
            'refresh_token':str(refresh_token),
            'access_token':str(refresh_token.access_token)
    }


class RegistrationApiView(APIView):
    # permission_classes = [IsAuthenticated,IsSuperUser]
    def post(self,request):
        serialized_data = RegistrationSerializer(data=request.data)

        if serialized_data.is_valid():
            user = serialized_data.save()
            return Response(
                {
                    "id":user.id,
                    "login":user.login,
                    "name":user.name,
                    "role":user.role,
                    "stores":user.stores.values_list('id',flat=True),
                    "image":request.build_absolute_uri(user.image.url)

                }
            )
        else:
            return Response(serialized_data.errors,status = status.HTTP_400_BAD_REQUEST)

class LoginApiView(APIView):
    def post(self,request):
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid():
            user = authenticate(**serializer.validated_data)
            if user is None:
                return Response({'message':"User not found"},status =  status.HTTP_404_NOT_FOUND)
            else:
                response = Response()
                token = get_token_for_user(user)
                response.set_cookie(
                    key = settings.SIMPLE_JWT['AUTH_COOKIE'],
                    value=token['access_token'],
                    expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                    path="/",
                    domain=None,
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                )
                response.set_cookie(
                    key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
                    value=token['refresh_token'],
                    expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                    path="/",
                    domain=None,
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                )
                response.data = serializer.data

                return response
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class TestApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        return Response(
            {
                "message":'Hello world'
            }
        )