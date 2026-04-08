from django import template

register = template.Library()

@register.simple_tag
def get_categories():
    categories = [
        {'id': 1, 'name': 'Концерты'},
        {'id': 2, 'name': 'Театры'},
        {'id': 3, 'name': 'Выставки'},
        {'id': 4, 'name': 'Фестивали'},
        {'id': 5, 'name': 'Спектакли'},
    ]
    return categories

@register.simple_tag(name='total_events')
def get_total_events_count():
    return 24


@register.simple_tag
def multiply(a, b):
    return a * b


@register.simple_tag
def get_venue_name(venue_id):
    venues = {
        1: 'Казанская филармония',
        2: 'Драматический театр',
        3: 'Галерея современного искусства',
    }
    return venues.get(venue_id, 'Площадка не найдена')

@register.inclusion_tag('webpages/list_categories.html')
def show_categories(cat_selected=0):
    categories = [
        {'id': 1, 'name': 'Концерты'},
        {'id': 2, 'name': 'Театры'},
        {'id': 3, 'name': 'Выставки'},
        {'id': 4, 'name': 'Фестивали'},
        {'id': 5, 'name': 'Спектакли'},
    ]
    return {
        'cats': categories,
        'cat_selected': cat_selected,
    }