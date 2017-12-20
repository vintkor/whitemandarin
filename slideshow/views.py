# -*- coding: utf-8 -*-
from django.db import models
from django.http import HttpResponse
from django.template import Context, loader
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.shortcuts import redirect, render, get_object_or_404
from .models import *


def home(request):
    slids = Slid.objects.filter(category__in=[1,2], published=1).order_by('ordering')
    return render(request, 'index.html', {'slids':slids})

def product(request, category, brand, product_slug)
