from django.contrib import admin
from .models import Todo

class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')

admin.site.register(Todo, TodoAdmin)