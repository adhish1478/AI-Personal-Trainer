from rest_framework import serializers
from .models import FoodItem, DailyMeal, MealIngredient


class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model= FoodItem
        fields= '__all__'


class ManualMealIngredientSerializer(serializers.ModelSerializer):
    food_item= serializers.PrimaryKeyRelatedField(queryset= FoodItem.objects.all())

    class Meta:
        model= MealIngredient
        fields = ['id', 'food_item', 'quantity', 'unit']

    def create(self, validated_data):
        food= validated_data['food_item']
        quantity= validated_data['quantity']

        validated_data.update({
            'name': food.name,
            'calories': round(food.calories * quantity, 2),
            'protein': round(food.protein * quantity, 2),
            'carbs': round(food.carbs * quantity, 2),
            'fats': round(food.fats * quantity, 2),
        })

        meal= self.context['meal']
        instance= MealIngredient.objects.create(meal= meal, **validated_data)
        meal.update_totals()
        return instance
    
    def update(self, instance, validated_data):
        if 'quantity' in validated_data:
            instance.quantity= validated_data['quantity']
            food= instance.food_item
            q= instance.quantity

            instance.calories = round(food.calories * q, 2)
            instance.protein = round(food.protein * q, 2)
            instance.carbs = round(food.carbs * q, 2)
            instance.fats = round(food.fats * q, 2)

            instance.save()
            instance.meal.update_totals()

        return instance
    
class AIMealIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model= MealIngredient
        fields= ['id', 'name', 'quantity', 'unit', 'calories', 'protein', 'carbs', 'fats']

    def create(self, validated_data):
        meal= self.context['meal']
        instance= MealIngredient.objects.create(meal= meal, **validated_data)
        # no need for re-calculating totals, since already provided by ai
        return instance
    
class ManualDailyMealSerializer(serializers.ModelSerializer):
    ingredients= ManualMealIngredientSerializer(many=True)

    class Meta:
        model= DailyMeal
        fields= ['id', 'date', 'user', 'meal_type', 'meal_name', 'source', 'ingredients']

    def create(self, validated_data):
        ingredients_data= validated_data.pop('ingredients')
        meal= DailyMeal.objects.create(**validated_data)

        for ingredient_data in ingredients_data:
            food = ingredient_data.get("food_item")
            # Force convert to ID
            if isinstance(food, dict):
                ingredient_data["food_item"] = food.get("id")
            elif isinstance(food, FoodItem):
                ingredient_data["food_item"] = food.pk

            serializer= ManualMealIngredientSerializer(data= ingredient_data, context= {'meal': meal})
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return meal
    
class AIDailyMealSerializer(serializers.ModelSerializer):
    ingredients= AIMealIngredientSerializer(many=True)

    class Meta:
        model= DailyMeal
        fields= ['id', 'date', 'user', 'meal_type', 'meal_name', 'source',
                  'calories', 'protein', 'carbs', 'fats', 'ingredients']
        
    def create(self, validated_data):
        ingredients_data= validated_data.pop('ingredients')
        meal= DailyMeal.objects.create(**validated_data)

        for ingredient_data in ingredients_data:
            serializer = AIMealIngredientSerializer(data=ingredient_data, context={'meal': meal})
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return meal


