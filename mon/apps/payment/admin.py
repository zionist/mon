from django.contrib import admin
from django import forms
from .models import Payment


class PaymentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Payment, PaymentAdmin)

