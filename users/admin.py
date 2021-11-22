from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    search_fields = [
        'fullname',
        'email'
    ]
    list_display = [
        'fullname',
        'email',
        'pure_phonenumber'
    ]