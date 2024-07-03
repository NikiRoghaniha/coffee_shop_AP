from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views import CreateUserView, ProfileView, OTPLoginView, OTPVerificationView, AdminCategoryViewSet, \
    AdminStorageViewSet, AdminProductViewSet, HomePageView, CategoryListingView, AddToCartView

router = DefaultRouter()
router.register(r'admin/categories', AdminCategoryViewSet, basename='admin-categories')
router.register(r'admin/storages', AdminStorageViewSet)
router.register(r'admin/products', AdminProductViewSet)
router.register(r'categories', CategoryListingView)

urlpatterns = [
    path('user/', CreateUserView.as_view(), name='create-user'),
    path('token/obtain/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('otp-login/', OTPLoginView.as_view(), name='otp-login'),
    path('otp-verify/', OTPVerificationView.as_view(), name='otp-verify'),
    path('home-page/', HomePageView.as_view(), name='home-page'),
    path('cart/add/', AddToCartView.as_view(), name='add-to-cart'),
]
