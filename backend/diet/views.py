from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from .models import FoodItem, DailyMeal, MealIngredient
from .serializers import FoodItemSerializer, AIDailyMealSerializer, AIMealIngredientSerializer, ManualDailyMealSerializer, ManualMealIngredientSerializer 
# AUTH and Permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import NotAuthenticated


# Bulk Food items upload
class FoodItemListCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        items= FoodItem.objects.all()
        serializer= FoodItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        data= request.data
        if isinstance(data, dict):
            # Single item creation
            serializer= FoodItemSerializer(data=data)
        else:
            # Bulk creation
            serializer= FoodItemSerializer(data=data, many=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Change Daily Meals, including ingredients
class DailyMealCreateDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


    def post(self, request):
        data = request.data
        data['user'] = request.user.id
        serializer= ManualDailyMealSerializer(data=data)

        if serializer.is_valid():
            daily_meal = serializer.save()
            return Response(ManualDailyMealSerializer(daily_meal).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, meal_id):
        try:
            meal = DailyMeal.objects.get(id=meal_id, user=request.user)
        except DailyMeal.DoesNotExist:
            return Response({'error': 'Meal not found.'}, status=status.HTTP_404_NOT_FOUND)

        meal.delete()
        return Response({'message': 'Meal deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    

class DailyMealRetrieveView(RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = DailyMeal.objects.all()
    serializer_class = ManualDailyMealSerializer
    lookup_field = 'id'

    def get_queryset(self):
        # Ensure only the requesting user's meals can be viewed
        return DailyMeal.objects.filter(user=self.request.user)
    
    
class SaveAIMealView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        data['source'] = 'ai'
        data['user'] = request.user.id
        serializer = AIDailyMealSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'AI meal saved successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateDeleteMealIngredient(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = MealIngredient.objects.all()
    serializer_class = ManualMealIngredientSerializer
    lookup_field = 'id'

    '''def get_queryset(self):
        return MealIngredient.objects.filter(meal__user=self.request.user)'''
    
    def get_queryset(self):
        user = self.request.user
        if not user or not user.is_authenticated:
            raise NotAuthenticated(detail="Authentication credentials were not provided or are invalid.")
        return MealIngredient.objects.filter(meal__user=user)
