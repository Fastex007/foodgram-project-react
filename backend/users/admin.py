from django.contrib import admin

from users.models import Follow


class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author')
    search_fields = ('user', 'author')
    list_filter = ('user', 'author')
    empty_value_display = '-пусто-'


admin.site.register(Follow, FollowAdmin)
