from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'verified')  
    list_filter = ('is_staff', 'verified')  
    search_fields = ('username', 'email')
    actions = ['verify_users']

    def verify_users(self, request, queryset):
        queryset.update(verified=True)
        self.message_user(request, "Selected users have been verified.")
    verify_users.short_description = "Mark selected users as verified"