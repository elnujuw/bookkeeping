# Register your models here.
from django.contrib import admin
from .models import *


class BookkeepingRecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'date', 'type', 'amount', 'category', 'description']
    search_fields = ['date', 'type', 'amount', 'category', 'description']
    ordering = ['id']

class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'key_hash']
    ordering = ['id']




admin.site.register(BookkeepingRecord, BookkeepingRecordAdmin)
admin.site.register(ApiKey, ApiKeyAdmin)