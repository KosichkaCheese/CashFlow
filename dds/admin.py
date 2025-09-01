from django.contrib import admin
from .models import Category, SubCategory, CashFlow, Status, OperationType

# добавляем в админку управление таблицами


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'slug']


@admin.register(OperationType)
class OperationTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'slug']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'operation_type', 'is_active']
    list_filter = ['operation_type', 'is_active']
    search_fields = ['name', 'slug']


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'slug']


@admin.register(CashFlow)
class CashFlowAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'status', 'operation_type',
                    'category', 'subcategory', 'amount', 'comment']
    list_filter = ['created_at', 'status',
                   'operation_type', 'category', 'subcategory']
    search_fields = ['created_at', 'status', 'operation_type',
                     'category', 'subcategory', 'amount', 'comment']
    date_hierarchy = 'created_at'
