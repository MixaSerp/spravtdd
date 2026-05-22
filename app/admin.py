# app/admin.py
from django.contrib import admin
from .models import Term

@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ('name', 'gost_name')
    search_fields = ('name', 'definition', 'gost_name')