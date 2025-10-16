from django.contrib import admin
from .models import FoodItem, DailyMeal, MealIngredient
# Register your models here.

admin.site.register(FoodItem)

# ---- Meal ingredient -----
class MealIngredientAdmin(admin.ModelAdmin):
    list_display = ('meal', 'name', 'quantity', 'get_user','meal__id', 'meal__source')

    def get_user(self, obj):
        return obj.meal.user.email
    get_user.short_description = 'User'

admin.site.register(MealIngredient, MealIngredientAdmin)

# ---- DailyMeal- Tabular view----

class MealIngredientInline(admin.TabularInline):
    model= MealIngredient
    extra= 1
class DailyMealAdmin2(admin.ModelAdmin):
    inlines = [MealIngredientInline]
    list_display = ('user', 'meal_type', 'source','date')
    search_fields = ('user__email',)
    ordering = ('date',)
    list_filter = ('source', 'date')
admin.site.register(DailyMeal, DailyMealAdmin2)
