from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from .serializer import UserSerializer, LoginSerializer
from .models import User
from django.contrib.auth import authenticate
from rest_framework import permissions
from rest_framework.generics import CreateAPIView


class SignUp(CreateAPIView):
    """
    Used for sign up only for manager. It will store data in user datatable and send JWT token in response.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def post(self, request, *args):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'errors': serializer.errors})
        serializer.save()
        user = User.objects.get(username=serializer.data['username'])
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'status': status.HTTP_200_OK,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'payload': serializer.data,
                'message': "Data saved successfully."
            })
        else:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': 'User not found'})


class Login(CreateAPIView):
    """
    Used for Login In manager only employee can't login.
    If email i.e username and password are correct then it will send JWT token in response.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args):
        username = request.data['username']
        password = request.data["password"]
        user = authenticate(username=username, password=password)

        if user is None:
            raise AuthenticationFailed("User Not Found")
        if not user.is_manager:
            raise AuthenticationFailed("Employee can't login")
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
