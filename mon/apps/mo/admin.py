from django.contrib import admin
from django import forms
from .models import MO, RegionalBudget, FederalBudget, Subvention, DepartamentAgreement, Orphan, PeopleAmount


class MOAdmin(admin.ModelAdmin):
    pass

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

class DepartamentAgreementAdmin(admin.ModelAdmin):
    pass

admin.site.register(DepartamentAgreement, DepartamentAgreementAdmin)


class OrphanAdmin(admin.ModelAdmin):
    pass

admin.site.register(Orphan, OrphanAdmin)


class PeopleAmountAdmin(admin.ModelAdmin):
    pass

admin.site.register(PeopleAmount, PeopleAmountAdmin)
