from django.contrib import admin
from django import forms
from .models import Ground, Building, CopyBuilding


class GroundAdmin(admin.ModelAdmin):
    pass

admin.site.register(Ground, GroundAdmin)


class BuildingAdmin(admin.ModelAdmin):
    pass

admin.site.register(Building, BuildingAdmin)


class CopyBuildingAdmin(admin.ModelAdmin):
    pass

admin.site.register(CopyBuilding, CopyBuildingAdmin)
