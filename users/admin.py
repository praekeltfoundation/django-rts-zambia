from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from models import UserDistrict

class UserDistrictInline(admin.StackedInline):
    model = UserDistrict
    max_num = 1


class UserAdmin(UserAdmin):
    inlines = (UserDistrictInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
