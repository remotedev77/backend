from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Permission

from my_app.models import User, Direction
from users.models import Company, AdminTable
from users.forms import *
# Register your models here.


@admin.register(AdminTable)
class AdminModelAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff','is_superuser', 'is_active')


@admin.register(Direction)
class DirectionModelAdmin(admin.ModelAdmin):
    list_display = ['name']


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances

    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'first_name', 'last_name', 'father_name', 'final_test','start_date', 'end_date', 'access',
                    'organization', 'is_admin', 'is_staff', 'is_superuser', 'is_active', 'main_test_count', 'direction_type')
    list_filter = ('is_admin',)
    # search_fields = []
    # autocomplete_fields = ["organization"]
    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name', 'father_name','final_test','role','direction_type',
                    'organization', 'password', 'main_test_count','start_date', 'end_date', 'access')}),
        
        ('Permissions', {'fields': ('is_admin','is_staff', 'is_superuser','groups','is_active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2','father_name', 'final_test',
                    'organization', 'is_admin', 'is_staff','groups','is_superuser', 'is_active', 'main_test_count',
                    'start_date', 'end_date', 'access', 'role'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ("groups",)




# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
admin.site.register(Company)
admin.site.register(Permission)