from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password= None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email= self.normalize_email(email)
        user= self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using= self._db)
        return user
    
    def create_superuser(self, email, password= None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)
    
class CustomUser(AbstractUser):
    username= None
    email= models.EmailField(unique=True)
    is_active= models.BooleanField(default=True)
    is_staff= models.BooleanField(default=False)
    is_verified= models.BooleanField(default=False)
    created_at= models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS= []

    objects= CustomUserManager()

    def __str__(self):
        return self.email

class UserProfile(models.Model):

    GENDER_CHOICES = [('male', 'Male'), ('female', 'Female'), ('other', 'Other')]
    ACTIVITY_LEVEL_CHOICES = [
        ('sedentary', 'Sedentary (little or no exercise)'),
        ('lightly_active', 'Lightly active (light exercise/sports 1-3 days/week)'),
        ('moderately_active', 'Moderately active (moderate exercise/sports 3-5 days/week)'),
        ('very_active', 'Very active (hard exercise/sports 6-7 days a week)'),
        ('extra_active', 'Extra active (very hard exercise/sports & physical job or training twice a day)')
    ]
    GOAL_CHOICES = [
    ("lose_1kg", "Lose 1 kg/week"),
    ("lose_0.75kg", "Lose 0.75 kg/week"),
    ("lose_0.5kg", "Lose 0.5 kg/week"),
    ("lose_0.25kg", "Lose 0.25 kg/week"),
    ("maintain", "Maintain weight"),
    ("lean_bulk", "Lean bulk"),
    ("gain_0.25kg", "Gain 0.25 kg/week"),
    ("gain_0.5kg", "Gain 0.5 kg/week"),
    ("gain_0.75kg", "Gain 0.75 kg/week"),
    ("gain_1kg", "Gain 1 kg/week"),
]

    user= models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    first_name= models.CharField(max_length=30, blank=True)
    last_name= models.CharField(max_length=30, blank=True)
    age= models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    # Physical attributes
    height= models.FloatField(null=True, blank=True) # in cm
    weight= models.FloatField(null=True, blank=True) # in kg
    activity_level= models.CharField(max_length=20, choices=ACTIVITY_LEVEL_CHOICES, default='sedentary')
    lifts_weight= models.BooleanField(default=False) # Whether the user lifts weights
    body_fat= models.FloatField(null=True, blank=True)
    # Goals and calorie targets
    goal= models.CharField(max_length=20, choices=GOAL_CHOICES, default='maintain') # Default to maintain weight
    maintenance_cals= models.IntegerField(null= True)
    goal_cals= models.IntegerField(null=True)

    # Macronutrient targets
    carbs= models.IntegerField(null=True)
    protein= models.IntegerField(null=True)
    fats= models.IntegerField(null=True)
    fibre= models.IntegerField(null=True)

    # Dietary preferences
    allergies= models.JSONField(default=list, blank=True)
    cuisine= models.CharField(max_length=50, blank=True, null=True)

    created_at= models.DateField(auto_now_add=True)
    updated_at= models.DateField(auto_now= True)
    # status
    is_profile_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email}'s Profile"
    
    class Meta:
        verbose_name= "User Profile"
        verbose_name_plural= "User Profiles"

    def get_activity_factor(self):
        level_map= {
        'sedentary': 1.2,
        'lightly_active': 1.375,
        'moderately_active': 1.55,
        'very_active': 1.725,
        'extra_active': 1.9
    }
        return level_map.get(self.activity_level, 1.2) # Default to sedentary if not found

    def calculate_maintenance_calories(self):
        """
        Calculates BMR (Basal Metabolic Rate) using the Mifflin-St Jeor Equation.
        Returns estimated daily maintenance calories assuming sedentary activity.
        """
        if not all([self.weight, self.height, self.age, self.gender]):
            return None # Incomplete data
        
        weight= self.weight
        height= self.height
        age= self.age

        if self.gender == 'female':
            bmr= 10 * weight + 6.25 * height - 5 * age - 161
        else:
            bmr= 10 * weight + 6.25 * height - 5 * age + 5

        activity_factor= self.get_activity_factor()
        return round(bmr*activity_factor)
    

    def calculate_goal_calories(self):
        """
        Calculates goal calories based on the user's goal.
        """
        if not self.maintenance_cals:
            return None
        
        goal_map= {
            'lose_1kg': -1000,
            'lose_0.75kg': -750,
            'lose_0.5kg': -500,
            'lose_0.25kg': -250,
            'maintain': 0,
            'lean_bulk': 250,
            'gain_0.25kg': 250,
            'gain_0.5kg': 500,
            'gain_0.75kg': 750,
            'gain_1kg': 1000
        }
        
        return self.maintenance_cals + goal_map.get(self.goal, 0)
    
    def calculate_macros(self):
        """
        Calculates macronutrient targets based on goal calories.
        Returns a dictionary with carb, protein, fat, and fibre targets.
        """

        if not self.weight or not self.goal_cals:
            return None # Incomplete data

        weight= self.weight
        goal= self.goal
        lifts= self.lifts_weight


        # ---- Protein Logic -----
        if lifts:
            if goal.startswith('lose'):
                protein_per_kg= 2.0
            elif goal == 'lean_bulk':
                protein_per_kg= 1.9
            elif goal.startswith('gain'):
                protein_per_kg= 1.7
            else:
                protein_per_kg= 1.6

        else:
            protein_per_kg= 1.2

        self.protein = round(weight * protein_per_kg)

        # ----- Fat Percentage Logic -------
        if goal.startswith('lose'):
            fat_pct= 0.22
        elif goal.startswith('maintain'):
            fat_pct= 0.25
        else: # bulk or lean bulk
            fat_pct= 0.20

        fat_cals= self.goal_cals * fat_pct
        self.fats= round(fat_cals/9)

        # ----- Carbohydrate Logic ------ (Remaining cals after protein and fats)
        protein_cals= self.protein * 4
        fat_cals= self.fats * 9
        carbs_cals= self.goal_cals - protein_cals - fat_cals

        self.carbs= round(carbs_cals/4)


        # ------- Fibre Logic ---------
        if self.gender == 'female':
            self.fibre = 25 if self.goal_cals < 2200 else 28
        else:
            self.fibre = 30 if self.goal_cals < 2500 else 35

    def update_profile_completion(self):
        mandatory = [self.age, self.gender, self.height, self.weight, self.activity_level, self.goal]
        self.is_profile_completed = all(v is not None and v != "" for v in mandatory)
    @property
    def is_ready_for_meal_plan(self):
        """Convenience property for frontend"""
        return self.is_profile_completed and self.goal_cals is not None

    def save(self, *args, **kwargs):
        self.maintenance_cals= self.calculate_maintenance_calories()
        self.goal_cals= self.calculate_goal_calories()
        self.calculate_macros()
        self.update_profile_completion()
        super().save(*args, **kwargs)