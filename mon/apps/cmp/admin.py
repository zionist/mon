from django.contrib import admin
from django import forms
from .models import CompareData, Result, Person, Auction
from apps.build.models import Contract, ContractDocuments
from apps.imgfile.models import File, Image


class AuctionAdmin(admin.ModelAdmin):
    pass

admin.site.register(Auction, AuctionAdmin)


class CompareDataAdmin(admin.ModelAdmin):
    pass

admin.site.register(CompareData, CompareDataAdmin)


class ContractDocumentsAdmin(admin.ModelAdmin):
    pass

admin.site.register(ContractDocuments, ContractDocumentsAdmin)


class ContractAdmin(admin.ModelAdmin):
    pass

admin.site.register(Contract, ContractAdmin)


class PersonAdmin(admin.ModelAdmin):
    pass

admin.site.register(Person, PersonAdmin)


class ResultAdmin(admin.ModelAdmin):
    pass

admin.site.register(Result, ResultAdmin)
