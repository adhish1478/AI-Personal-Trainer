from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView # type: ignore
from .views import CustomUserViewSet, UserProfileViewSet
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router= DefaultRouter()
router.register(r'profiles', UserProfileViewSet, basename= 'profile')


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
    path('api/register/', CustomUserViewSet.as_view(), name='custom_user'),
   
]