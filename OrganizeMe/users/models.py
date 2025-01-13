import random
import string
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)  # To track email verification
    verification_code = models.CharField(max_length=6, blank=True, null=True)

    def generate_verification_code(self):
        """Generate a random 6-digit verification code."""
        self.verification_code = ''.join(random.choices(string.digits, k=6))
        self.save()

    USERNAME_FIELD = 'email'  # Log in with email instead of username
    REQUIRED_FIELDS = ['username']  # Username is still required





class BlacklistedToken(models.Model):
    token = models.CharField(max_length=500, unique=True)
    blacklisted_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def add(cls, token):
        cls.objects.create(token=str(token))

    @classmethod
    def is_blacklisted(cls, token):
        return cls.objects.filter(token=str(token)).exists()
