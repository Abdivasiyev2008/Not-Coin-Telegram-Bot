# botapp/admin.py

from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ['telegram_id', 'coins', 'limit', 'energy', 'tap', 'sub']
    search_fields = ['telegram_id']

    def save_model(self, request, obj, form, change):
        obj.refill_limit()  # Bu yerda avtomatik ravishda limitni yangilash chaqiriladi
        super().save_model(request, obj, form, change)

admin.site.register(User, UserAdmin)
