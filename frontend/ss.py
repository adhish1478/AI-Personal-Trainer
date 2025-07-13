from rest_framework import serializers
from .models import FoodItem, DailyMeal, MealIngredient


class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model= FoodItem
        fields= '__all__'

class MealIngredientSerializer(serializers.Serializer):
    # Used in both cases
    name = serializers.CharField(required= False)
    quantity = serializers.FloatField()
    unit = serializers.CharField(default='grams')

    # Optional if source is 'manual' (we fetch from FoodItem)
    food_item = serializers.PrimaryKeyRelatedField(
        queryset=FoodItem.objects.all(), required=False
    )

    # Required if source is 'ai'
    calories = serializers.FloatField(required=False)
    protein = serializers.FloatField(required=False)
    carbs = serializers.FloatField(required=False)
    fats = serializers.FloatField(required=False)

    def validate(self, data):
        source = self.context.get("source")

        if source == 'manual':
            if 'food_item' not in data or 'quantity' not in data:
                raise serializers.ValidationError(
                    "For manual entries, 'food_item' and 'quantity' are required."
                )
            food = data['food_item']
            quantity = data['quantity']
            data['name'] = food.name  # ✅ Fix: Inject name here
            data['calories'] = food.calories * quantity
            data['protein'] = food.protein * quantity
            data['carbs'] = food.carbs * quantity
            data['fats'] = food.fats * quantity

        elif source == 'ai':
            required_fields = ['calories', 'protein', 'carbs', 'fats']
            for field in required_fields:
                if field not in data:
                    raise serializers.ValidationError(
                        f"For AI entries, '{field}' is required."
                    )
        return data
    def create(self, validated_data):
        # ✅ You must define this
        meal = self.context.get('meal')  # We will pass this in .save(meal=meal)
        return MealIngredient.objects.create(meal=meal, **validated_data)
    
class DailyMealSerializer(serializers.ModelSerializer):
    ingredients = MealIngredientSerializer(many=True)

    class Meta:
        model = DailyMeal
        fields = ['id', 'date', 'user', 'meal_type', 'meal_name', 'source', 'ingredients']

    def validate(self, data):
        source = data.get("source")

        for i, ingredient in enumerate(data.get("ingredients", [])):
            # 🛠️ Fix potential instance bug if manually nested
            if source == 'manual' and isinstance(ingredient.get('food_item'), FoodItem):
                ingredient['food_item'] = ingredient['food_item'].id

            serializer = MealIngredientSerializer(data=ingredient, context={'source': source})
            serializer.is_valid(raise_exception=True)
        return data

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        source = validated_data.get('source')
        meal = DailyMeal.objects.create(**validated_data)

        for ingredient in ingredients_data:
            serializer = MealIngredientSerializer(data=ingredient, context={'source': source, 'meal': meal})
            serializer.is_valid(raise_exception=True)
            serializer.save()  # No meal passed here anymore, it's already in context
        return meal

