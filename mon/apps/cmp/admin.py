from django.contrib import admin
from django import forms
from .models import CompareData, Contract, Result, Person, Auction
from apps.imgfile.models import File, Image


class CompareDataAdmin(admin.ModelAdmin):
    pass

admin.site.register(CompareData, CompareDataAdmin)


class ContractAdmin(admin.ModelAdmin):
    pass

admin.site.register(Contract, ContractAdmin)


class PersonAdmin(admin.ModelAdmin):
    pass

admin.site.register(Person, PersonAdmin)


class ResultAdmin(admin.ModelAdmin):
    pass

admin.site.register(Result, ResultAdmin)


class AuctionAdmin(admin.ModelAdmin):
    pass

admin.site.register(Auction, AuctionAdmin)
