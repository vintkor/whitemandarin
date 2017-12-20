from django.contrib import admin
from .models import *
from content.fields import AdminImageWidget
from django.db import models


class SlidAdmin(admin.ModelAdmin):
    list_display = ('name', 'pic', 'published', 'ordering')
    list_editable = ('published', 'ordering')
    formfield_overrides = {
        models.ImageField: {'widget': AdminImageWidget},
    }
admin.site.register(Slid, SlidAdmin)


admin.site.register(Category)
