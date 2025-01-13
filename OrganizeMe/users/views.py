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
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
import threading  # For handling blacklisting in the background
import logging
import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken
import threading
import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from asgiref.sync import sync_to_async
import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken


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








logger = logging.getLogger(__name__)

class LogoutView(GenericAPIView):
    permission_classes = [AllowAny]  # No authentication required for logout

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"error": "Refresh token is missing."}, status=status.HTTP_400_BAD_REQUEST)

        # Log the token received
        logger.info(f"Received token for logout: {refresh_token}")

        # Send the response before token processing
        response = Response({"message": "User logged out successfully."}, status=status.HTTP_205_RESET_CONTENT)

        try:
            # Blacklist the refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.info(f"Successfully blacklisted token: {refresh_token}")
        except Exception as e:
            logger.error(f"Failed to blacklist token: {refresh_token}. Error: {e}")

        return response

