from django.contrib import admin

from django.contrib import admin
from .models import Usuario, Fisico
from django.contrib.auth.admin import UserAdmin

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Informações adicionais', {'fields': ('idade', 'telefone', 'tipo')}),
    )
    list_display = ('username', 'email', 'tipo', 'is_staff', 'is_superuser')
    list_filter = ('tipo', 'is_staff', 'is_superuser')

