# -*- coding: utf-8 -*-
from django.db import models
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import auth
from django.views.decorators.cache import never_cache

# from HTMLParser import HTMLParser
from shop.models import *
from content.models import *
from .models import *


@never_cache
def addtowishlist(request):
    id = request.POST.get('id', 0)

    product = get_object_or_404(Product, pk=id)
    if id and request.user.is_authenticated:
        if request.user.whishlist:
            if product.id in request.user.whishlist:
                request.user.whishlist.remove(product.id)
            else:
                request.user.whishlist.append(product.id)
        else:
            request.user.whishlist = [product.id]
        request.user.save()
    return HttpResponse('ok')


@never_cache
def profile(request):
    return render(request, "profile.html")


@never_cache
def viewed(request):
    if request.user.is_authenticated:
        items = Product.objects.filter(pk__in=request.user.viewed)
        return render(request, "viewed.html", {"name": u"Просмотренные акции", "items": items})
    else:
        redirect('/')


@never_cache
def addaction(request):
    return render(request, "addaction.html")


@never_cache
def settings(request):
    if request.user.is_authenticated:

        if request.method == "GET":
            return render(request, "settings.html")
        else:
            name = request.POST.get('name')
            lastname = request.POST.get('lastname')
            phone = request.POST.get('phone')
            address = request.POST.get('address')

            request.user.first_name = name
            request.user.last_name = lastname
            request.user.phone = phone
            request.user.address = address
            request.user.save()
            return render(request, "settings.html")

    else:
        redirect('/')



@never_cache
def whishlist(request):
    if request.user.is_authenticated:
        items = Product.objects.filter(pk__in=request.user.whishlist)
        return render(request, "viewed.html", {"name": u"В списке желаний", "items": items})
    else:
        redirect('/')


@never_cache
def order(request, id):
    item = get_object_or_404(Order, pk=id, user=request.user)

    return render(request, 'order.html', {'item': item })
    # pass


@never_cache
def orders(request):
    items = Order.objects.filter(user=request.user).order_by('-id')
    return render(request, 'orders.html', {'items': items})
