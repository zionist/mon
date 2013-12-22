from django.contrib import admin
from django import forms
from .models import Developer, Room, Kitchen, WC, Hallway, \
    AuctionRoom, AuctionKitchen, AuctionWC, AuctionHallway, Choices, \
    Choice


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


class AuctionRoomAdmin(admin.ModelAdmin):
    pass

admin.site.register(AuctionRoom, AuctionRoomAdmin)


class AuctionKitchenAdmin(admin.ModelAdmin):
    pass

admin.site.register(AuctionKitchen, AuctionKitchenAdmin)


class AuctionWCAdmin(admin.ModelAdmin):
    pass

admin.site.register(AuctionWC, AuctionWCAdmin)


class AuctionHallwayAdmin(admin.ModelAdmin):
    pass

admin.site.register(AuctionHallway, AuctionHallwayAdmin)


class ChoiceAdmin(admin.TabularInline):
    model = Choice


class ChoicesAdmin(admin.ModelAdmin):
    inlines = [ChoiceAdmin, ]

admin.site.register(Choices, ChoicesAdmin)

