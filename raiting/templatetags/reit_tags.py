from django import template
register = template.Library()

@register.inclusion_tag('rating/rating.html')
def reit(paket, model, id, reit, votes):
    
    return {'paket':paket, 'model':model, 'id':id, 'reit':reit, 'votes':votes}

