from django.contrib import admin
# Register your models here.
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from apps.user.models import APIUser

User = get_user_model()


class CustomUserAdmin(UserAdmin):
    pass


admin.site.register(User, CustomUserAdmin)
admin.site.register(APIUser, CustomUserAdmin)
