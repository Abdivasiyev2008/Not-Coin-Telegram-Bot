from django.contrib import admin
from django.core.paginator import Paginator

from .models import User, RefFriendModel

class UserAdmin(admin.ModelAdmin):
    list_display = ['telegram_id', 'coins', 'limit', 'energy', 'tap', 'sub']
    search_fields = ['telegram_id']

    def save_model(self, request, obj, form, change):
        obj.refill_limit()
        super().save_model(request, obj, form, change)


class InvFriendAdmin(admin.ModelAdmin):
    list_display = ['telegram_id', 'ref_friend']
    search_fields = ['telegram_id', 'ref_friend']


admin.site.register(User, UserAdmin)
admin.site.register(RefFriendModel, InvFriendAdmin)
