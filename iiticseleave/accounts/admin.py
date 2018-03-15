from django.contrib import admin
from django.contrib.auth import get_user_model
from .forms import UserAdmin
from django.contrib.auth.models import Group


# Register your models here.
User = get_user_model()

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
