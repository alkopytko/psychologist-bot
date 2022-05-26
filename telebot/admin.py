from django.contrib import admin

# Register your models here.
from telebot.models import Executor


@admin.register(Executor)
class ExecutorAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'first_name', 'last_name', 'approved')
    list_filter = ('approved',)
    # search_fields = ('author', 'text')
    actions = ['approve']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)