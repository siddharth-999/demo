from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import User, Family, FamilyRelation


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password', 'username')}),
        (_('Personal info'), {'fields': (
            'first_name', 'last_name', 'date_of_birth',
            'address',)}),
        (_('Permissions'), {'fields': (
            'is_active', 'is_superuser', 'is_staff')}),
        (_('Important dates'),
         {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ["id", "email", "is_active", ]

    list_filter = ('is_active',)

    ordering = ('-id',)

    search_fields = ('first_name', 'last_name', 'email')


class FamilyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class FamilyRelationAdmin(admin.ModelAdmin):
    list_display = ('id', 'added_by', 'relation', 'relative',)


admin.site.register(User, UserAdmin)
admin.site.register(Family, FamilyAdmin)
admin.site.register(FamilyRelation, FamilyRelationAdmin)
