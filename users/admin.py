from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from models import UserDistrict

class UserDistrictInline(admin.StackedInline):
    model = UserDistrict
    max_num = 1
    fk_name = 'user'


class UserAdmin(UserAdmin):
    list_display = ["username", "email", "first_name", "last_name",
                    "is_active", "date_joined", "is_staff"]
    inlines = (UserDistrictInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
