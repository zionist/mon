from django.contrib import admin
from django import forms
from .models import Image, File


class ImageAdmin(admin.ModelAdmin):
    pass

admin.site.register(Image, ImageAdmin)


class FileAdmin(admin.ModelAdmin):
    pass

admin.site.register(File, FileAdmin)
