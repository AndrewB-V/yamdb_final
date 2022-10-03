from users.models import User

from django.contrib import admin


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'role',
    )
    search_fields = ('username', 'email',)
    list_filter = ('username',)
