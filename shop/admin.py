from django.contrib import admin
from .models import *
# from adwords.models import *
# from django_extensions.admin imp-ort admin.ModelAdmin


class InlineFilterSelect(admin.StackedInline):
    model = FilterSelect

# class InlineProperty(admin.StackedInline):
#     model = Property


class InlinePhoto(admin.StackedInline):
    model = Photo
    extra = 1


class InlineColorProduct(admin.StackedInline):
    model = ColorProduct
    extra = 1


class InlineComplectItem(admin.StackedInline):
    model = ComplectItem
    extra = 1
# class InlineExtraProduct(admin.StackedInline):
#     model = ExtraProduct


class InlineExtraCategory(admin.StackedInline):
    model = ExtraCategory
    extra = 1


class InlineCategorySinonim(admin.StackedInline):
    model = CategorySinonim
    extra = 1


class InlineOrderProduct(admin.StackedInline):
    model = OrderProduct
    extra = 1


class InlineOrderColor(admin.StackedInline):
    model = OrderColor
    extra = 1


class InlineOrderPlace(admin.StackedInline):
    model = OrderPlace
    extra = 1


class InlineOrderComplect(admin.StackedInline):
    model = OrderComplect
    extra = 1


class InlineOrderDelivery(admin.StackedInline):
    model = OrderDelivery
    extra = 1


class OrderColorAdmin(admin.ModelAdmin):
    list_display = ('id', 'price')


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'proccessed',
        'name',
        'lastname',
        'allproducts',
        'phone',
        'email',
        'pub_date')
    list_editable = ('proccessed',)
    search_fields = ['name', 'phone', 'email']
    # prepopulated_fields = {"slug": ("name",)}
    # class Media:
        # js = ("suit/js/filters.js",)
        # InlineOrderProduct, InlineOrderColor, InlineOrderComplect,
    inlines = [InlineOrderPlace, InlineOrderDelivery]


class ComplectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    inlines = [InlineComplectItem]

    class Media:
        js = ("js/select2.js", "js/complect.js")
        css = {
            'all': ("css/select2.css",)
        }
    # def save_model(self, request, obj, form, change):
    #     assert False, obj.items


class FilterAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name',)
    search_fields = ('name',)
    list_per_page = 4000

    class Media:
        js = ("suit/js/filters.js",)
    inlines = [InlineFilterSelect]


class CategoryAdmin(admin.ModelAdmin):
    list_filter = ('parent', )
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'slug', 'hotlineurl', 'published', 'hotline', 'nadavi', 'priceua', 'ordering', 'column')
    list_editable = ('slug', 'published', 'hotline', 'nadavi', 'priceua', 'ordering', 'column')
    inlines = [InlineCategorySinonim,]
    # class Media:
    #     js = ("suit/js/category.js",)


class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_per_page = 4000

    # list_editable = ('name',)


class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'slug', 'published', 'ordering')
    list_editable = ('slug', 'published', 'ordering')
    search_fields = ('name',)
    list_per_page = 4000


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'idname', 'waranty', 'published', 'price', 'hotline', 'newproduct', 'nadavi', 'priceua', 'action_time')
    list_editable = ('waranty', 'published', 'hotline', 'newproduct', 'nadavi', 'priceua', 'action_time')
    list_filter = ('category', )
    list_per_page = 200
    inlines = [InlineColorProduct, InlineExtraCategory,]
    search_fields = ('id', 'name', 'idname', 'action',)
    exclude = ('colors', 'color_set', 'maincolor_id', 'search', 'ftssearch')
    raw_id_fields = ("extraproduct", 'giftproduct', 'recomendproduct')
    filter_horizontal = ('dopcategory',)

    class Media:
        js = ("/static_cdn/admin/js/underscore.js", "/static_cdn/admin/js/product.js",)

    # def save_model(self, request, obj, form, change):

    #     user = request.user
    #     instance = form.save(commit=False)
    #     product = instance.save()
    #     if change:
    #         pass
    #         # assert False, request.POST#.get('newselect[2]')
    #     filters = instance.category.filters.all()
    #     f = 0
    #     for filter in filters:
    #         if filter.filtertype == 4:
    #             items = request.POST.getlist(filter.slug + '_' + str(filter.id))
    #             if items:
    #                 f += 1
    #         if filter.filtertype == 3:
    #             item = request.POST.get(filter.slug + '_' + str(filter.id))
    #             if item:
    #                 f += 1

    #     if f:
    #         FilterItem.objects.filter(product = instance).delete()

    #     for filter in filters:
    #         if filter.filtertype == 4:
    #             items = request.POST.getlist(filter.slug + '_' + str(filter.id))
    #             for item in items:
    #                 filterselect = FilterItem(product = instance, filter = filter, value = item)
    #                 filterselect.save()
    #         if filter.filtertype == 3:
    #             item = request.POST.get(filter.slug + '_' + str(filter.id))
    #             # assert False, item
    #             if item:
    #                 filterselect = FilterItem(product = instance, filter = filter, value = item)
    #                 filterselect.save()

    #     propertys = instance.category.properties.all()
    #     p = 0
    #     for property in propertys:
    #         postprop = request.POST.get('property_' + str(property.id))
    #         if postprop:
    #             p += 1
    #     if p:
    #         PropertyProduct.objects.filter(product = instance).delete()

    #     for property in propertys:
    #         postprop = request.POST.get('property_' + str(property.id))

    #         if postprop and len(postprop):
    #             propitem = PropertyProduct(product = instance, property = property, value = postprop)
    #             propitem.save()

    #     return instance
    def save_model(self, request, obj, form, change):
        productfilters = []
        props = []

        user = request.user
        instance = form.save(commit=False)
        product = instance.save()
        if change:
            pass
            # assert False, request.POST#.get('newselect[2]')

        if instance.category:
            filters = instance.category.filters.all()

            for filter in filters:
                items = request.POST.getlist('filter_' + str(filter.id))

                # assert False, items
                for item in items:
                    productfilters.append(int(item))

            obj.filters = productfilters

            properties = instance.category.properties.all().order_by('ordering')
            for prop in properties:
                prophtml = request.POST.get('property_' + str(prop.id))
                props.append([prop.id, prop.name, prophtml])

            obj.properties = props
            obj.save()

        return instance

class QuikOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'proccessed', 'producttext', 'phone', 'pub_date')
    list_editable = ('proccessed',)
    search_fields = ['phone']
    exclude = ['product']


class NoOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'proccessed', 'producttext', 'phone', 'pub_date')
    list_editable = ('proccessed',)
    search_fields = ['phone']
    exclude = ['product']


class ArticlesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class SeoAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'fil')
    list_editable = ('category', 'fil')


class SeoBrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand')
    list_editable = ('category', 'brand')


class LowPriceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_editable = ('category', )


class PopularAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_editable = ('category', )


class ColorRGBAdmin(admin.ModelAdmin):
    list_display = ('name', 'rgb')
    list_editable = ('rgb', )

class ProxyAdmin(admin.ModelAdmin):
    list_display = ('name', 'active')
    list_editable = ('active', )

class FilterSeoAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'active', 'brand', 'fs1', 'fs2', 'fs3')
    list_editable = ('category', )
    search_fields = ('title',)
    list_per_page = 100


    class Media:
        js = ("suit/js/underscore.js", "suit/js/seofilter.js",)

class ConcurentAdmin(admin.ModelAdmin):
    list_display = ('itemid', 'name', 'strong')
    list_editable = ('strong', )
    search_fields = ('name', 'itemid')
    list_per_page = 100

class AncorAdmin(admin.ModelAdmin):
    list_display = ('id','ancor', 'url', 'published')
    list_editable = ("ancor", 'url', 'published')
    list_display_links = ('id',)
# class BrandDescriptionAdmin(admin.ModelAdmin):
#     list_display = ('title', 'brand', 'category')
#     search_fields = ['title', ]
# admin.site.register(BrandDescription, BrandDescriptionAdmin)

# class ColorProductAdmin(admin.ModelAdmin):
#     prepopulated_fields = {"slug": ("name",)}

# admin.site.register(ColorProduct, ColorProductAdmin)
admin.site.register(QuikOrder, QuikOrderAdmin)
admin.site.register(NoOrder, NoOrderAdmin)
admin.site.register(Filter, FilterAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Articles, ArticlesAdmin)
admin.site.register(Complect, ComplectAdmin)
admin.site.register(Seo, SeoAdmin)
admin.site.register(SeoBrand, SeoBrandAdmin)
admin.site.register(LowPrice, LowPriceAdmin)
admin.site.register(Popular, PopularAdmin)
admin.site.register(ColorRGB, ColorRGBAdmin)
admin.site.register(OrderColor, OrderColorAdmin)
admin.site.register(FilterSeo, FilterSeoAdmin)
admin.site.register(Statistica)
admin.site.register(Ucat)
admin.site.register(Concurent, ConcurentAdmin)
admin.site.register(Uproduct)
admin.site.register(ProxyList)
admin.site.register(Proxy, ProxyAdmin)
admin.site.register(Ancor, AncorAdmin)
# admin.site.register(Ecomerce)
