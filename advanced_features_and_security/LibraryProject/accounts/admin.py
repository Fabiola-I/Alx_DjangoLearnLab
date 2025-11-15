# advanced_features_and_security/LibraryProject/accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Adds the custom fields to the admin change form
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('date_of_birth', 'profile_photo')}),
    )
    # Adds the custom field to the user list view
    list_display = UserAdmin.list_display + ('date_of_birth',)
    
admin.site.register(CustomUser, CustomUserAdmin)