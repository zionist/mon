from django.contrib import admin
from django import forms
from .models import Building


class BuildingAdmin(admin.ModelAdmin):
    pass


admin.site.register(Building, BuildingAdmin)
