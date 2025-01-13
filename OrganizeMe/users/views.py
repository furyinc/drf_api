from .serializers import RegisterSerializer, VerifyEmailSerializer, LoginSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from .serializers import VerifyEmailSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer
import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LogoutSerializer


User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class VerifyEmailView(generics.GenericAPIView):
    serializer_class = VerifyEmailSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        code = serializer.validated_data['verification_code']

        user = User.objects.filter(email=email).first()
        if user and user.verification_code == code:
            user.is_verified = True
            user.is_active = True
            user.save()
            return Response({"message": "Email verified successfully!"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid verification code"}, status=status.HTTP_400_BAD_REQUEST)






class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # The validated_data now includes the refresh token, access token, and username
        response_data = serializer.validated_data

        return Response(response_data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        # Validate the refresh token
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Send success message before blacklisting the token
        response = Response(
            {"message": "User successfully logged out."},
            status=status.HTTP_205_RESET_CONTENT
        )

        # Blacklist the token after sending the response
        serializer.save()
        return response

# class LogoutView(generics.GenericAPIView):
#     permission_classes = [AllowAny]
#
#     def post(self, request):
#         # Extract the refresh token from the request body
#         refresh_token = request.data.get("refresh")
#         if not refresh_token:
#             return Response(
#                 {"error": "Refresh token is required."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#
#         # Send success message before blacklisting the token
#         response = Response(
#             {"message": "User successfully logged out."},
#             status=status.HTTP_205_RESET_CONTENT
#         )
#
#
#         # Blacklist the token (executed after sending the response)
#         try:
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#         except Exception:
#             pass  # Silently handle any exceptions during blacklisting
#
#         return response


