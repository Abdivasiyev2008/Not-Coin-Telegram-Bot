from django.contrib import admin
from .models import User, RefFriendModel


class UserAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'coins', 'limit', 'energy', 'tap', 'sub',)
    search_fields = ['telegram_id']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        for user in qs:
            user.refill_limit()
        return qs


class InvFriendAdmin(admin.ModelAdmin):
    list_display = ['telegram_id', 'ref_friend']
    search_fields = ['telegram_id', 'ref_friend']


admin.site.register(User, UserAdmin)
admin.site.register(RefFriendModel, InvFriendAdmin)
