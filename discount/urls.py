"""discount URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from shop import views as shop_views
from content import views as content_views
from pricelist import views as pricelist_views

# import comments
# from action.view

urlpatterns = [


    url(r'^allfiltershotline/$', pricelist_views.allfiltershotline, name='allfiltershotline'),
    url(r'^price/$', pricelist_views.price, name='price'),
    # url(r'^price/$', pricelist_views.price, name='price'),
    url(r'^getdropname/$', pricelist_views.getdropname, name='getdropname'),
    url(r'^getdropfile/$', pricelist_views.getdropfile, name='getdropfile'),
    url(r'^simplesearch/$', pricelist_views.simplesearch, name='simplesearch'),
    url(r'^createconnection/$', pricelist_views.createconnection, name='createconnection'),
    url(r'^get_filters_properties/(?P<id>[0-9]+)/$', pricelist_views.get_filters_properties, name='get_filters_properties'),
    url(r'^get_hotline_filters_properties/(?P<id>[_0-9a-zA-Z-]+)/$', pricelist_views.get_hotline_filters_properties, name='get_hotline_filters_properties'),
    url(r'^deletepropertiesfilters/$', pricelist_views.deletepropertiesfilters, name='deletepropertiesfilters'),
    url(r'^copypropertiesfilters/$', pricelist_views.copypropertiesfilters, name='copypropertiesfilters'),
 

    url(r'^allactions/$', shop_views.allactions, name='allactions'),
    url(r'^getactionbycat/(?P<id>[0-9]+)/$', shop_views.getactionbycat, name='getactionbycat'),
    url(r'^setaction/$', shop_views.setaction, name='setaction'),
    url(r'^clearcache/$', shop_views.clearcache, name='clearcache'),


    url(r'^allcomplects/$', shop_views.allcomplects, name='allcomplects'),
    url(r'^getcatcomplect/$', shop_views.getcatcomplect, name='getcatcomplect'),
    url(r'^getcattree/$', shop_views.getcattree, name='getcattree'),
    url(r'^createcomplect/$', shop_views.createcomplect, name='createcomplect'),
    url(r'^deletecomplect/$', shop_views.deletecomplect, name='deletecomplect'),
    url(r'^ugcsv/$', shop_views.ugcsv, name='ugcsv'),
    url(r'^$', content_views.home, name='home'),
    url(r'^amp/$', content_views.home),
    url(r'^seopage/$', shop_views.seopage, name='seopage'),
    url(r'^seometa/$', shop_views.seometa, name='seometa'),
    url(r'^seokey/$', shop_views.seokey, name='seokey'),
    url(r'^doc/$', shop_views.getdocument, name='getdoc'),
    url(r'^real_time_price/(?P<id>[0-9]+)/$', shop_views.real_time_price, name='real_time_price'),

    url(r'^delete_phrase/$', shop_views.delete_phrase, name='delete_phrase'),
    url(r'^get_nodes/$', shop_views.get_nodes, name='get_nodes'),
    url(r'^writecaptcha/$', shop_views.writecaptcha, name='writecaptcha'),
    url(r'^importcsv/$', shop_views.importcsv, name='importcsv'),
    url(r'^get_one_node/$', shop_views.get_one_node, name='get_one_node'),
    url(r'^get_category_filters/$', shop_views.get_category_filters, name='get_category_filters'),

    url(r'^get_cities/$', shop_views.get_cities, name='get_cities'),
    url(r'^get_warehouses/$', shop_views.get_warehouses, name='get_warehouses'),

     url(r'^robots.txt$', content_views.robots, name='robots'),
     url(r'^googleb5f4fe133172dd00.html$', content_views.google, name='google'),

     url(r'^20k.xml$', shop_views.sitemap, name='sitemap'),
     url(r'^ecomerce/$', shop_views.ecomerce, name='ecomerce'),
     url(r'^yml.xml$', shop_views.yml, name='yml'),
     url(r'^hotline/$', shop_views.hotline, name='hotline'),
     url(r'^nadavi/$', shop_views.nadavi, name='nadavi'),
     url(r'^priceua/$', shop_views.priceua, name='priceua'),
     url(r'^hotline.xml$', shop_views.hotline_xml, name='hotline_xml'),
     url(r'^nadavi.xml$', shop_views.nadavi_xml, name='nadavi_xml'),
     url(r'^priceua.xml$', shop_views.priceua_xml, name='priceua_xml'),
     url(r'^action/$', shop_views.action, name='action'),
     url(r'^action/page-(?P<page>[0-9]+)/$', shop_views.action, name='action2'),
     url(r'^top20/$', shop_views.top20, name='top20'),
     url(r'^createmenu/$', shop_views.createmenu, name='createmenu'),
     url(r'^discount/$', shop_views.discount, name='discount'),
     url(r'^discount/page-(?P<page>[0-9]+)/$', shop_views.discount, name='discount2'),
     url(r'^dublies/$', shop_views.dublies, name='dublies'),

     url(r'^clear_cache/$', content_views.clear_cache, name='clear_cache'),
     url(r'^page/(?P<slug>[_0-9a-zA-Z-]+)/$', content_views.page, name='page'),
     url(r'^manager/$', shop_views.manager, name='manager'),


     url(r'^usfull/$', content_views.usfull, name='usfull'),
     url(r'^usfull/(?P<slug>[_0-9a-zA-Z-]+)/$', content_views.usfull_item, name='usfull_item'),

     url(r'^akcii/$', content_views.akcii, name='akcii'),
     url(r'^akcii/(?P<slug>[_0-9a-zA-Z-]+)/$', content_views.akcya, name='akcya'),
     url(r'^overviews/(?P<slug>[_0-9a-zA-Z-]+)/$', content_views.page, name='page'),
     url(r'^overviews/$', content_views.overviews, name='overviews'),
     #url(r'^wwww/$', shop_views.wwwwqqqq', name='wwww'),
     url(r'^test/$', shop_views.prod_list, name='prod_list'),
     # url(r'^get_user/$', 'accounts.views.get_user', name='get_user'),
     # url(r'^get_user_ajax/$', 'accounts.views.get_user_ajax', name='get_user_ajax'),
     url(r'^search/$', shop_views.search, name='search'),
     url(r'^export/$', shop_views.export, name='export'),
     url(r'^export_orders/$', shop_views.export_orders, name='export_orders'),
     url(r'^google_feed/$', shop_views.google_feed, name='google_feed'),
     url(r'^karta-sajta/$', shop_views.karta_sajta, name='karta_sajta'),
     # url(r'^test2/$', shop_views.product', name='product'),
    # url(r'^cms/', include('cms.foo.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    # # (r'^page/',include('content.urls')),
    # (r'^tinymce/',include('tinymce.urls')),
    # (r'^media/tiny_mce/',include('tinymce.urls')),



    # url(r'^reb/', include('reb.foo.urls')),


    # url(r'^fishca_admin/filebrowser/', include(site.urls)),
    url(r'^goadmin/', include(admin.site.urls)),

    url(r'^accounts/', include('allauth.urls')),
    url(r'^profile/', include('profile.urls')),
    url(r'^redactor/', include('redactor.urls')),

    # url(r'^shop_admin/', include(shop.urls)),
    # url(r'^clear_cache/$', shop_views.clear_cache', name='clear_cache'),
    url(r'^oneclick/$', shop_views.oneclick, name='oneclick'),
    url(r'^noclick/$', shop_views.noclick, name='moclick'),

    url(r'^add_to_cart/(?P<id>[0-9]+)/$', shop_views.add_to_cart, name='add_to_cart'),
    url(r'^add_to_cart_one/(?P<id>[0-9]+)/$', shop_views.add_to_cart_one, name='add_to_cart_one'),
    url(r'^add_to_cart/(?P<id>[0-9]+)/(?P<color>[0-9]+)/$', shop_views.add_to_cart, name='add_to_cart2'),
    url(r'^add_complect/(?P<id>[0-9]+)/$', shop_views.add_complect, name='add_complect'),
    url(r'^add_complect/(?P<id>[0-9]+)/(?P<color>[0-9]+)/$', shop_views.add_complect, name='add_complect'),
    url(r'^show_cart/$', shop_views.show_cart, name='show_cart'),
    url(r'^change_cart/$', shop_views.change_cart, name='change_cart'),
    url(r'^checkout/step1/$', shop_views.step1, name='step1'),
    url(r'^checkout/thanx/$', shop_views.thanx, name='thanx'),
    url(r'^checkout/step2/$', shop_views.step2, name='step2'),
    url(r'^comments/', include('comments.urls')),

    url(r'^compare/$', shop_views.compare, name='compare'),
    url(r'^clear_compare/$', shop_views.clear_compare, name='clear_compare'),
    url(r'^compare_list/$', shop_views.compare_list, name='compare_list'),
    url(r'^to-compare/(?P<category_id>[0-9]+)/$', shop_views.to_compare, name='to_compare'),

    url(r'^reit/', include('raiting.urls')),
    url(r'^hot/', include('hotline.urls')),


    url(r'^get_filters/(?P<id>[_0-9]+)/$', shop_views.get_filters_by_cat, name='get_filters_by_cat'),
    url(r'^get_filters/(?P<id>[_0-9]+)/(?P<product_id>[_0-9]+)/$', shop_views.get_filters_by_cat, name='get_filters_by_cat'),

    url(r'^catalog/(?P<category>[_0-9a-zA-Z-]+)/(?P<fil>[_0-9a-zA-Z-]+)/$', shop_views.seo, name='seo'),
    url(r'^category/(?P<category>[_0-9a-zA-Z-]+)/(?P<brand>[_0-9a-zA-Z-]+)/$', shop_views.seobrand, name='seobrand'),

    url(r'^nedorogo/(?P<category>[_0-9a-zA-Z-]+)/$', shop_views.nedorogo, name='nedorogo'),
    url(r'^poplyarnue/(?P<category>[_0-9a-zA-Z-]+)/$', shop_views.poplyarnue, name='poplyarnue'),

    url(r'^get_properties/(?P<id>[_0-9]+)/$', shop_views.get_properties_by_cat, name='get_properties_by_cat'),
    url(r'^get_properties/(?P<id>[_0-9]+)/(?P<product_id>[_0-9]+)/$', shop_views.get_properties_by_cat, name='get_properties_by_cat'),
    #url(r'^(?P<category>[-a-z0-9_]+)/$', shop_views.vhod_clas', name='vhod_clas'),
    url(r'^brand/(?P<slug>[_0-9a-zA-Z-]+)/$', shop_views.brand, name='brand'),
    url(r'^(?P<slug>[_0-9a-zA-Z-]+)/amp/$', shop_views.category, name='category'),
    url(r'^(?P<category>[_0-9a-zA-Z-]+)/(?P<brand>[_0-9a-zA-Z-]+)/$', shop_views.brandcategory, name='brandcategory'),
    url(r'^(?P<category>[_0-9a-zA-Z-]+)/(?P<brand>[_0-9a-zA-Z-]+)/amp/$', shop_views.brandcategory, name='brandcategory2'),
    url(r'^(?P<category>[_0-9a-zA-Z-]+)/(?P<brand>[_0-9a-zA-Z-]+)/(?P<product_slug>[_0-9a-zA-Z-]+)/$', shop_views.product, name='product'),
    url(r'^(?P<category>[_0-9a-zA-Z-]+)/(?P<brand>[_0-9a-zA-Z-]+)/(?P<product_slug>[_0-9a-zA-Z-]+)/amp/$', shop_views.product, name='product2'),
    url(r'^(?P<category>[_0-9a-zA-Z-]+)/(?P<brand>[_0-9a-zA-Z-]+)/(?P<product_slug>[_0-9a-zA-Z-]+)/(?P<color_slug>[0-9]+)/$', shop_views.product, name='product'),
    url(r'^(?P<slug>[_0-9a-zA-Z-]+)/$', shop_views.category, name='category'),


]


# assert False, settings.STATIC_URL

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
