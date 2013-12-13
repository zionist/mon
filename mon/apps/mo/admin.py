from django.contrib import admin
from django import forms
from .models import MO, RegionalBudget, FederalBudget, Subvention, DepartamentAgreement, Orphan, PeopleAmount


class DepartamentAgreementInline(admin.TabularInline):
    model = DepartamentAgreement
    extra = 1


class PeopleAmountInline(admin.TabularInline):
    model = PeopleAmount
    extra = 1


class MOAdmin(admin.ModelAdmin):
    inlines = [DepartamentAgreementInline, PeopleAmountInline]

admin.site.register(MO, MOAdmin)


class RegionalBudgetAdmin(admin.ModelAdmin):
    pass

admin.site.register(RegionalBudget, RegionalBudgetAdmin)


class FederalBudgetAdmin(admin.ModelAdmin):
    pass

admin.site.register(FederalBudget, FederalBudgetAdmin)


class SubventionAdmin(admin.ModelAdmin):
    pass

admin.site.register(Subvention, SubventionAdmin)


class OrphanAdmin(admin.ModelAdmin):
    pass

admin.site.register(Orphan, OrphanAdmin)
