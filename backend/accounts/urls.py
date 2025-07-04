from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView # type: ignore
from .views import CustomUserViewSet, UserProfileViewSet
from rest_framework.routers import DefaultRouter




urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', CustomUserViewSet.as_view(), name='custom_user'),
    path('api/profile/', UserProfileViewSet.as_view(), name='user_profile'),
   
]