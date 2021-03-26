from django import template
from django.urls import reverse

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css, })


@register.simple_tag
def food_tag_link(request, meal=None):
    """
    Создать кверистринг при включении/выключении/переключении тегов.
    При создании учитывается существование пагинации
    (т.е. в кверистринг уже может быть ключ page, который нельзя дублировать)
    """
    query_string = request.GET.copy()
    tags = query_string.getlist('tag')
    if not meal:
        if not tags:
            return ''
        query_string.pop('page', None)
        return f"&{query_string.urlencode()}"
    if meal in tags:
        tags.remove(meal)
        if not tags and not query_string.get('page'):
            # избавляемся от одинокого "?" после снятия всех тегов
            redirect_url = request.resolver_match.view_name
            kwargs = request.resolver_match.kwargs
            return reverse(redirect_url, kwargs=kwargs)
        query_string.setlist('tag', tags)
    else:
        query_string.appendlist('tag', meal)
    return f'?{query_string.urlencode()}'
