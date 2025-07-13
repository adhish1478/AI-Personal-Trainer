from django.db import models
from accounts.models import CustomUser
from django.utils import timezone
from datetime import date

MEAL_CHOICES= [
    ('breakfast', 'Breakfast'),
    ('lunch', 'Lunch'),
    ('dinner', 'Dinner'),
    ('snack', 'Snack'),
]

class FoodItem(models.Model):
    name= models.CharField(max_length= 255)
    calories= models.FloatField()
    protein= models.FloatField()
    carbs= models.FloatField()
    fats= models.FloatField()
    fiber= models.FloatField(null=True, blank=True)  # Optional field for fiber content

    def __str__(self):
        return self.name

class DailyMeal(models.Model):
    date= models.DateField(default=date.today)
    user= models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    meal_type= models.CharField(max_length=10, choices=MEAL_CHOICES)
    meal_name= models.CharField(max_length=255)
    source= models.CharField(max_length=255, choices= [('manual', 'Manual'), ('ai', 'AI')], default='manual') # for tracking purposes

    # 🆕 Store totals
    calories = models.FloatField(default=0)
    protein = models.FloatField(default=0)
    carbs = models.FloatField(default=0)
    fats = models.FloatField(default=0)

    def update_totals(self):
        self.calories = sum(i.calories for i in self.ingredients.all())
        self.protein = sum(i.protein for i in self.ingredients.all())
        self.carbs = sum(i.carbs for i in self.ingredients.all())
        self.fats = sum(i.fats for i in self.ingredients.all())
        self.save()
    
    def __str__(self):
        return f"{self.meal_type.capitalize()} - {self.meal_name} on {self.date} for {self.user.username}"
    
class MealIngredient(models.Model):
    meal= models.ForeignKey(DailyMeal, related_name='ingredients', on_delete=models.CASCADE)

    # Used only for manual meal entries
    food_item = models.ForeignKey(FoodItem, null=True, blank=True, on_delete= models.SET_NULL)

    # Always Used
    name= models.CharField(max_length=255)
    quantity= models.FloatField()  # Quantity in grams or as appropriate
    unit= models.CharField(max_length=50, default='grams')  # e.g., grams, ml, etc.

    # Always required, either fetched from DB or directly provided by AI
    calories= models.FloatField()
    protein= models.FloatField()
    carbs= models.FloatField()
    fats= models.FloatField()

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit}) in {self.meal.meal_name} on {self.meal.date} for {self.meal.user.username}"

