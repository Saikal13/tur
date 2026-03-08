from django.contrib import admin
from .models import AdminLog, AdminComment


@admin.register(AdminLog)
class AdminLogAdmin(admin.ModelAdmin):
    list_display = ['admin', 'booking', 'action', 'created_at']
    list_filter = ['action', 'created_at']
    search_fields = ['admin__username', 'booking__name']
    readonly_fields = ['created_at']


@admin.register(AdminComment)
class AdminCommentAdmin(admin.ModelAdmin):
    list_display = ['admin', 'booking', 'created_at']
    list_filter = ['created_at']
    search_fields = ['admin__username', 'booking__name', 'comment']
    readonly_fields = ['created_at', 'updated_at']