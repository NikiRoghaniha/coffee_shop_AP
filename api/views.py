import os
import random
import httpx
from django.core.cache import cache
from django.db.models import Sum
from rest_framework import generics, status, viewsets, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from api import models
from api.models import User, Category, Storage, Product, HomePageSlider, Order
from api.serializers import UserSerializer, OTPLoginSerializer, OTPVerificationSerializer, CategorySerializer, \
    StorageSerializer, ProductSerializer, HomePageSliderSerializer, CategoryListSerializer, CategoryProductsSerializer, \
    AddToCartSerializer, OrderSerializer, PayOrderSerializer

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


class AdminCategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]


class AdminStorageViewSet(viewsets.ModelViewSet):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer
    permission_classes = [IsAdminUser]


class AdminProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]


class HomePageView(generics.ListAPIView):
    MOST_SOLD_PRODUCT_COUNT = 12
    serializer_class = HomePageSliderSerializer

    def get_queryset(self):
        return HomePageSlider.objects.filter(active=True).order_by('sort')

    def get_most_sold_products(self):
        return Product.objects.annotate(
            total_sold=Sum('orderitem__quantity', filter=models.Q(orderitem__order__is_paid=True))
        ).order_by('-total_sold')[:self.MOST_SOLD_PRODUCT_COUNT]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        products_serializer = ProductSerializer(self.get_most_sold_products(), many=True)
        return Response({'slider': serializer.data, 'most_sold_products': products_serializer.data})


class CategoryListingView(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Category.objects.all()
    lookup_field = 'name'

    def get_serializer_class(self):
        if self.action == 'list':
            return CategoryListSerializer
        elif self.action == 'retrieve':
            return CategoryProductsSerializer


class AddToCartView(generics.CreateAPIView):
    serializer_class = AddToCartSerializer
    permission_classes = [IsAuthenticated]


class CartView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Order, user=self.request.user, is_paid=False)


class PayOrderView(generics.UpdateAPIView):
    serializer_class = PayOrderSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Order, user=self.request.user, is_paid=False)

    def perform_update(self, serializer):
        serializer.validated_data['is_paid'] = True
        serializer.save()
