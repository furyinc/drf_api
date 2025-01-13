from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
import random
from django.core.mail import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from rest_framework import serializers, generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.permissions import AllowAny


User = get_user_model()


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    verification_code = serializers.CharField(max_length=6)  # Change to CharField



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        # Get the user by email
        user = User.objects.filter(email=email).first()

        # Check if the user exists and the password is correct
        if not user or not user.check_password(password):
            raise serializers.ValidationError("Invalid credentials")

        # Ensure the user is verified
        if not user.is_verified:
            raise serializers.ValidationError("Email not verified")

        # Generate tokens using SimpleJWT
        tokens = RefreshToken.for_user(user)

        # Return tokens and the username
        return {
            'refresh': str(tokens),
            'access': str(tokens.access_token),
            'username': user.username  # Include username in the response
        }



class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.is_active = False  # Deactivate until email is verified
        user.save()

        # Generate verification code
        verification_code = random.randint(1000, 9999)
        user.verification_code = verification_code
        user.save()

        # HTML email content with styled verification code
        html_message = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Email Verification</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 20px auto;
                    background-color: #fff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                }}
                h2 {{
                    color: #333;
                    text-align: center;
                }}
                .verification-code {{
                    font-size: 48px;
                    font-weight: bold;
                    color: #1E90FF;
                    text-align: center;
                    padding: 10px;
                    border: 2px solid #1E90FF;
                    border-radius: 8px;
                    margin-top: 20px;
                }}
                .message {{
                    color: #555;
                    font-size: 16px;
                    line-height: 1.5;
                    text-align: center;
                }}
                .footer {{
                    font-size: 14px;
                    color: #777;
                    text-align: center;
                    margin-top: 30px;
                }}
                .footer a {{
                    color: #1E90FF;
                    text-decoration: none;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2 style="font-family: 'Poppins', sans-serif; font-weight: 600;">📬Pochta Manzilini Tasdiqlash</h2>
                <p class="message">Assalomu alaykum! Ro'yxatdan o'tishni tasdiqlash uchun kod:</p>
                <div class="verification-code">{verification_code}</div>
                <div class="footer">
                    <p>Agar savollaringiz bo'lsa biz bilan <a href="mailto:frilancer029@gmail.com">bog'laning</a>.</p>
                </div>
            </div>
        </body>
        </html>
        """

        # Send the email with custom sender name and email
        sender_name = "OrganizeMe"  # Your website name
        sender_email = "frilancer029@gmail.com"  # Your support email address
        from_email = f"{sender_name} <{sender_email}>"

        email = EmailMessage(
            'TASDIQLASH KODI',  # Subject
            html_message,  # HTML message
            from_email,  # From email with custom sender name
            [user.email],  # To email
        )
        email.content_subtype = 'html'  # Specify that the content is HTML
        email.send()

        return user


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': 'Token is expired or invalid'
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')