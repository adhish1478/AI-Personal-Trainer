from django.shortcuts import render
from .models import CustomUser, UserProfile
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .serializers import CustomUserSerializer, UserProfileSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
# Create your views here.


User= get_user_model()
class CustomUserViewSet(APIView):
    '''
    ViewSet for CustomUser model
    '''
    permission_classes = [AllowAny]
    def post(self, request):
        data= request.data
        if User.objects.filter(email= data.get('email')).exists():
            return Response({"error": "User with this email already exists."}, status=400)
        
        serializer= CustomUserSerializer(data=data)
        if serializer.is_valid():
            user= serializer.save()
            return Response({
                "message": "User created successfully.",
                "user": user.email
            }, status=201)
        return Response(serializer.errors, status=400)
    
    

class UserProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

