from django.contrib import admin
from .models import *

class InlineFileProvider(admin.StackedInline):
    model = FileProvider
    extra = 1



class ProviderAdmin(admin.ModelAdmin):
    # prepopulated_fields = {"slug": ("name",)}
    list_display = ('name',)
    search_fields = ('name',)
    list_per_page = 200

    inlines = [InlineFileProvider]

    class Media:
        js = ("/static_cdn/admin/js/underscore.js", "/static_cdn/admin/js/provider.js",)


class PriceStringAdmin(admin.ModelAdmin):
    list_display = ('model', 'articul', 'brand', 'provider',  'description', 'linked', 'changed', 'garantee', 'price', 'price_grn', 'price_grn_rrc')        
    search_fields = ('searchindex',)
    

# Register your models here.
admin.site.register(Currency)
admin.site.register(Provider, ProviderAdmin)
admin.site.register(PriceString, PriceStringAdmin)
admin.site.register(FileProvider)#, FileProviderAdmin)
