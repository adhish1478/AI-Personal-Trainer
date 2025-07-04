from .models import CustomUser, UserProfile
from rest_framework import serializers

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model= CustomUser
        fields= ('id', 'email','password', 'is_active', 'is_staff', 'is_verified', 'created_at')
        read_only_fields= ('id', 'created_at')

    def create(self, validated_data):
        password= validated_data.pop('password', None)
        user= CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    full_name= serializers.SerializerMethodField()

    class Meta:
        model= UserProfile
        fields= ['id', 'first_name', 'last_name', 'full_name', 'age', 'gender', 'height',
            'weight', 'activity_level', 'maintanance_cals', 'goal_cals',
            'goal','lifts_weight', 'carbs', 'protein', 'fats', 'fibre', 'allergies', 'cuisine',
            'created_at', 'updated_at']
        read_only_fields= ['id', 'maintanance_cals', 'created_at', 'updated_at']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()
    
    def validate(self, data):
        if data.get('age') is not None and data['age'] < 0:
            raise serializers.ValidationError("Age cannot be negative.")
        if data.get('height') is not None and data['height'] <= 0:
            raise serializers.ValidationError("Height must be a positive number.")
        if data.get('weight') is not None and data['weight'] <= 0:
            raise serializers.ValidationError("Weight must be a positive number.")
        return data
    
    def create(self, validated_data):
        profile= UserProfile.objects.create(**validated_data)
        return profile
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
