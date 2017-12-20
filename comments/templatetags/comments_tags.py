from django import template
register = template.Library()


@register.inclusion_tag('comments/comments.html')
def comments(paket, item_model, item_id):
    from comments.models import Comments
    exec "from %s.models import %s" % (paket, item_model)
    p = eval("%s.objects.get(pk=%d)" % (item_model, int(item_id.id)))
    nodes = Comments.objects.filter(
        paket=paket, item_model=item_model, item_id=item_id.id, published=1
    ).order_by('-id')
    return {
        'nodes': nodes,
        'item': p,
        'paket': paket,
        'item_model': item_model,
        'item_id': item_id,
    }


@register.inclusion_tag('tags/comment.html')
def comment(one, com_class=False, item_id=False, show=False):
    # assert False, one
    return {'one': one, 'com_class': com_class, 'show': show, 'item_id': item_id}


@register.inclusion_tag('tags/comment_form.html')
def comment_form(one, type='review'):
    # assert False, one
    return {'one': one, 'type': type}
