from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User, Share


@admin.register(User)
class UserModelAdmin(UserAdmin):
    model = User
    search_fields = ['first_name', 'last_name', 'phone']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(Share)
class ShareAdmin(admin.ModelAdmin):
    model = Share
    ordering = ['order']
    search_fields = ['owner__first_name', 'owner__last_name']
    list_display = ['owner', 'order', 'asset']