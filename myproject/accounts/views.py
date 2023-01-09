from django.shortcuts import render
from rest_framework import views, response, exceptions, permissions

from .models import UserService
from .authentication import JWTAuthentication

user_service = UserService()

class RegisterApi(views.APIView):
    
    def post(self, request):
        user = user_service.create_user(
            first_name=request.data['first_name'],
            last_name=request.data['last_name'],
            email=request.data['email'],
            password=request.data['password'] if 'password' in request.data else None
        )
        return response.Response(data=user)


class LoginApi(views.APIView):
    def post(self, request):
        email=request.data['email']
        password=request.data['password']
        user = user_service.get_user(email)
        if user is None or not user.check_password(raw_password=password):
            raise exceptions.AuthenticationFailed('Invalid Credentials')
        token = user_service.create_token(user_id=user.id)
        resp = response.Response()
        resp.set_cookie(key="jwt", value=token, httponly=True)
        return resp 


class UserApi(views.APIView):
    authentication_classes = (JWTAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        user = request.user
        return response.Response(user)


class LogoutApi(views.APIView):
    authentication_classes = (JWTAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        resp = response.Response()
        resp.delete_cookie('jwt')
        resp.data = {'message': 'so long farewell'}
        return resp