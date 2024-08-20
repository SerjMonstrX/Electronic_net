from django.contrib import admin
from django.contrib.auth.models import Group
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'is_moderator', )
    list_filter = ('is_active', 'is_moderator')
    search_fields = ('email', 'is_active')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_moderator')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    def is_moderator(self, obj):
        return obj.groups.filter(name='moderators').exists()
    is_moderator.boolean = True
    is_moderator.short_description = 'Is Moderator'


admin.site.unregister(Group)


class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_count')

    def user_count(self, obj):
        return obj.user_set.count()
    user_count.short_description = 'Number of Users'


admin.site.register(Group, GroupAdmin)
