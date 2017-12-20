# -*- coding: utf-8 -*-
from django.db import models
from django.http import HttpResponse
from django.template import Context, loader
from content.models import Article, Category
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.shortcuts import redirect, render
from .models import Comments, Utility
from raiting.models import Reit
import json
from django.db.models import Avg, Max, Min, Count, Sum

def comment_save(request):
    if request.method == 'POST':
        paket = request.POST['paket']
        item_model = request.POST['item_model']
        item_id = request.POST['item_id']
        name = request.POST['name']
        text = request.POST['text']
        vote = request.POST['vote'] or 0
        exec "from %s.models import %s" % (paket, item_model)
        c = Comments(paket=paket, vote=float(vote), item_model=item_model, item_id=int(item_id), name=name, text=text, published=0)
        c.save()
        
        s = Reit(vote=float(vote), item_id=int(item_id), paket=paket, model_name=item_model)
        s.save()
        d = Reit.objects.filter(item_id=int(item_id), paket=paket, model_name=item_model).aggregate(total_votes=Sum('vote'), count_votes=Count('vote'))
        count_votes = d['count_votes'] + 1
        votes = float(d['total_votes']) + float(vote)
        rrr = votes/count_votes
        
        count_comments = Comments.objects.filter(paket=paket, item_model=item_model, item_id=int(item_id)).count()
        p = eval("%s.objects.get(pk=%d)" % (item_model, int(item_id)))
        p.comments_count = count_comments
        p.reit = rrr
        p.count_votes = count_votes
        p.save()
        c.prod_name = p.name 
        c.save()

    return HttpResponse("Ok")

def save_answer(request):
    if request.method == 'POST':
        paket = request.POST['paket']
        item_model = request.POST['item_model']
        item_id = request.POST['item_id']
        name = request.POST['name']
        text = request.POST['text']
        id = int(request.POST['id'])
        parent = Comments.objects.get(pk=id)
        vote =  0
        exec "from %s.models import %s" % (paket, item_model)
        c = Comments(paket=paket, vote=float(vote), parent=parent, item_model=item_model, item_id=int(item_id), name=name, text=text, published=0)
        c.save()
        
        
        
        
        count_comments = Comments.objects.filter(paket=paket, item_model=item_model, item_id=int(item_id)).count()
        p = eval("%s.objects.get(pk=%d)" % (item_model, int(item_id)))
        p.comments_count = count_comments
        
        p.save()

    return HttpResponse("Ok")


def utility(request):
    if request.method == 'POST':
        id = int(request.POST['id'])
        positive = int(request.POST['positive']) or 0
        c = Comments.objects.get(pk=id)
        u = Utility(comment=c, positive=positive)
        u.save()
        plus = Utility.objects.filter(comment=c, positive=1).count()
        minus = Utility.objects.filter(comment=c, positive=0).count()
        c.positive = plus
        c.negative = minus
        c.save()
    return HttpResponse("Ok")

