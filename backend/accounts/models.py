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

    user= models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    first_name= models.CharField(max_length=30, blank=True)
    last_name= models.CharField(max_length=30, blank=True)
    age= models.PositiveIntegerField(null=True, blank=True)
    gender= gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)

    height= models.FloatField() # in cm
    weight= models.FloatField() # in kg
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
        verbouse_name= "User Profile"
        verbouse_name_plural= "User Profiles"

    def calculate_maintanance_calories(self):
        """
        Calculates BMR (Basal Metabolic Rate) using the Mifflin-St Jeor Equation.
        Returns estimated daily maintenance calories assuming sedentary activity.
        """
        if not self.weight or self.height or self.age or self.gender:
            return None # Incomplete data
        
        weight= self.weight
        height= self.height
        age= self.age

        if self.gender == 'female':
            bmr= 10 * weight + 6.25 * height - 5 * age - 161
        else:
            bmr= 10 * weight + 6.25 * height - 5 * age + 5

        activity_factor= 1.2 # For sedentary lifestyle, can be changed later
        return(bmr*activity_factor)