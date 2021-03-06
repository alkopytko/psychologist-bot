from django.contrib import admin

# Register your models here.
from telebot.models import Executor, Client, ClientRequest

admin.site.register(Client)
admin.site.register(ClientRequest)

@admin.register(Executor)
class ExecutorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'approved')
    list_filter = ('approved',)
    # actions = ['approve']
    #
    # def approve(self, request, queryset):
    #     queryset.update(approved=True)




    # search_fields = ('author', 'text')
