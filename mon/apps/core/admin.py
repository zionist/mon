from django.contrib import admin
from django import forms
from .models import Developer, Room, Kitchen, WC, Hallway


class DeveloperAdmin(admin.ModelAdmin):
    pass

admin.site.register(Developer, DeveloperAdmin)


class RoomAdmin(admin.ModelAdmin):
    pass

admin.site.register(Room, RoomAdmin)


class KitchenAdmin(admin.ModelAdmin):
    pass

admin.site.register(Kitchen, KitchenAdmin)


class WCAdmin(admin.ModelAdmin):
    pass

admin.site.register(WC, WCAdmin)


class HallwayAdmin(admin.ModelAdmin):
    pass

admin.site.register(Hallway, HallwayAdmin)
