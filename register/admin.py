from django.contrib import admin

from .models import Customer


@admin.register(Customer)
class AdvUserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email', 'role')
    list_display_links = ['pk', 'username']
