from django.contrib import admin
from users.models import User

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'date_joined','father_name', 'main_test_count', 'is_admin', 'is_active', 'is_staff', 'is_superuser']
# Register your models here.
