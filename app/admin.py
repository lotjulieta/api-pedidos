from django.contrib import admin
from .models import (
    User,
    Scheme,
    Company,
    Pedido,
    Tecnico,
)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'email', 
        'full_name', 
        'is_active', 
        'is_staff'
    ]

@admin.register(Scheme)
class SchemeAdmin(admin.ModelAdmin):
    list_display = [
        'name'
    ]

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'phone',
        'email',
        'website'
    ]

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = [
        'type_request',
        'client',
        'scheme',
        'tecnico',
        'hours_worked'
    ]

@admin.register(Tecnico)
class TecnicoAdmin(admin.ModelAdmin):
    list_display = [
        'full_name',
        'phone',
        'email'
    ]
