from django.contrib import admin
from leave.models import Application
from leave.forms import ApplicationAdmin


# Register your models here.

admin.site.register(Application, ApplicationAdmin)
