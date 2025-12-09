from django.contrib import admin
from .models import Fisico
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class FisicoInline(admin.StackedInline):
    model = Fisico
    can_delete = False
    verbose_name_plural = "Dados físicos"

class UserAdmin(BaseUserAdmin):
    inlines = (FisicoInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
