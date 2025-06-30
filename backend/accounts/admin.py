from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, UserProfile

# CustomUserAdmin setup
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('email', 'is_staff', 'is_active', 'is_verified', 'created_at')
    list_filter = ('is_staff', 'is_active', 'is_verified')
    search_fields = ('email',)
    ordering = ('email',)
    readonly_fields = ('created_at',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified')}),
        ('Important Dates', {'fields': ('last_login', 'created_at')}),
        ('Groups & Permissions', {'fields': ('groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

# ✅ Merged UserProfileAdmin setup
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user_email',
        'user_first_name',
        'user_last_name',
        'age',
        'maintanance_cals',
        'goal_cals'
    )
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'allergies', 'cuisine')
    list_filter = ('gender', 'activity_level')
    readonly_fields = ('maintanance_cals', 'goal_cals', 'created_at', 'updated_at')

    def user_email(self, obj):
        return obj.user.email
    user_email.admin_order_field = 'user__email'
    user_email.short_description = 'Email'

    def user_first_name(self, obj):
        return obj.user.first_name
    user_first_name.admin_order_field = 'user__first_name'
    user_first_name.short_description = 'First Name'

    def user_last_name(self, obj):
        return obj.user.last_name
    user_last_name.admin_order_field = 'user__last_name'
    user_last_name.short_description = 'Last Name'

# Register CustomUser model
admin.site.register(CustomUser, CustomUserAdmin)