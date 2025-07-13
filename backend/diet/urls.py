from django.urls import path
from .views import (    FoodItemListCreateView,
    DailyMealCreateDeleteView,
    DailyMealRetrieveView,
    SaveAIMealView,
    UpdateDeleteMealIngredient
)

urlpatterns = [
    path('food-items/', FoodItemListCreateView.as_view(), name='fooditem-list-create'),
    path('meals/create/', DailyMealCreateDeleteView.as_view(), name='dailymeal-create'),
    path('meals/<int:id>/', DailyMealRetrieveView.as_view(), name='dailymeal-retrieve'),
    path('meals/create/ai/', SaveAIMealView.as_view(), name='ai-meal-save'),
    path("meal/delete/<int:meal_id>/", DailyMealCreateDeleteView.as_view()),
    path("meal-ingredient/<int:id>/", UpdateDeleteMealIngredient.as_view(), name="update-delete-ingredients")
]