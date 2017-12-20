# -*- coding: utf-8 -*-
from django.db import models
from django.http import HttpResponse
from django.template import Context, loader
from content.models import Article, Category
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.shortcuts import redirect, render
from .models import Reit
import json
from django.db.models import Avg, Max, Min, Count, Sum



def reit(request, paket, model_name, item_id):
    exec "from %s.models import %s" % (paket, model_name)
    if not 'score' in request.POST:
        return HttpResponse("Ошибка запроса")
    score = request.POST['score']
    s = Reit(vote=float(score), item_id=int(item_id), paket=paket, model_name=model_name)
    s.save()
    d = Reit.objects.filter(item_id=int(item_id), paket=paket, model_name=model_name).aggregate(total_votes=Sum('vote'), count_votes=Count('vote'))
    count_votes = d['count_votes'] + 1
    votes = float(d['total_votes']) + float(score)
    rrr = votes/count_votes
    prod = eval(" %s.objects.get(pk=%d)" % (model_name, int(item_id)))
    prod.reit = rrr
    prod.count_votes = count_votes
    prod.save()

    res = dict(msg=u'Спасибо. Ваш голос учтен', status='OK')
    r = HttpResponse(json.dumps(res), content_type="application/json")

    return r


