import os
import random
import httpx
from django.core.cache import cache
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import User
from api.serializers import UserSerializer, OTPLoginSerializer, OTPVerificationSerializer

KAVENEGAR_API_URL = f"https://api.kavenegar.com/v1/{os.getenv('KAVENEGAR_API_KEY')}/sms/send.json"


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileView(generics.UpdateAPIView, generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class OTPLoginView(generics.CreateAPIView):
    serializer_class = OTPLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data.get('phone_number')
        if not User.objects.filter(phone_number=phone_number).exists():
            return Response({"message": "User not found."}, status=status.HTTP_400_BAD_REQUEST)
        if self.send_otp(phone_number):
            return Response({"message": "OTP sent."})
        else:
            return Response({"message": "Failed to send OTP."}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def send_otp(phone_number):
        otp = str(random.randint(100000, 999999))
        cache.set(phone_number, otp, 120)
        data = {
            "receptor": phone_number,
            "message": otp,
        }
        with httpx.Client() as client:
            response = client.post(KAVENEGAR_API_URL, data=data)
            return response.status_code == status.HTTP_200_OK


class OTPVerificationView(generics.CreateAPIView):
    serializer_class = OTPVerificationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data.get('phone_number')
        try:
            user = User.objects.get(phone_number=phone_number)
            if serializer.validated_data.get('otp') == cache.get(phone_number):
                refresh = RefreshToken.for_user(user)
                cache.delete(phone_number)
                return Response({
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                })
            else:
                return Response({"message": "OTP verification failed."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"message": "User not found."}, status=status.HTTP_400_BAD_REQUEST)
