from django.contrib import admin
from .models import Comments

from django.db import models

class CommentsAdmin(admin.ModelAdmin):
    list_display = ('name', 'prod_name', 'text', 'paket', 'vote', 'date_add',  'published',)
    list_editable = ('vote', 'published', 'date_add',  )
    
admin.site.register(Comments, CommentsAdmin)