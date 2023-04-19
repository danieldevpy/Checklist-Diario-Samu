
from django.contrib import admin

from .models import User

# Register your models here.
class AdminUser(admin.ModelAdmin):
    list_display = ('username', 'unity', 'usa', 'usb', 'is_staff', 'is_superuser')
    list_filter = ('unity__name',)
    list_editable = ('unity', 'usa', 'usb')


admin.site.register(User, AdminUser)