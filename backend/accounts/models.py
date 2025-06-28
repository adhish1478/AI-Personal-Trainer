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

    user= models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    first_name= models.CharField(max_length=30, blank=True)
    last_name= models.CharField(max_length=30, blank=True)
    age= models.PositiveIntegerField(null=True, blank=True)
    gender= gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)

    height= models.FloatField(null=True, blank=True) # in cm
    weight= models.FloatField(null=True, blank=True) # in kg
    activity_level= models.CharField(max_length=20, choices=ACTIVITY_LEVEL_CHOICES, default='sedentary')
    maintanance_cals= models.IntegerField(null= True)
    goal_cals= models.IntegerField(null=True)
    body_fat= models.FloatField(null=True, blank=True)
    carb= models.FloatField(null=True)
    protein= models.FloatField(null=True)
    fat= models.FloatField(null=True)
    fibre= models.FloatField(null=True)
    allergies= models.JSONField(default=list, blank=True)
    cuisine= models.CharField(max_length=50, blank=True, null=True)

    created_at= models.DateField(auto_now_add=True)
    updated_at= models.DateField(auto_now= True)

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

    def calculate_maintanance_calories(self):
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
    
    def save(self, *args, **kwargs):
        self.maintanance_cals= self.calculate_maintanance_calories()
        super().save(*args, **kwargs)