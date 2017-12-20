from django.contrib import admin
from content.models import *


class MenuItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'menu', 'slug', 'published', 'ordering')
    list_editable = ('slug', 'published', 'ordering')


class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = (
        'name', 'slug', 'category', 'slug', 'published', 'ordering')
    list_editable = ('slug', 'published', 'ordering')


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


# class BannerAdmin(admin.ModelAdmin):
#     list_display = ('name', 'ordering', 'link', 'active')
#     list_editable = ('link', 'ordering', 'active')




admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Menu)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Snipet)
# admin.site.register(Banner, BannerAdmin)
