from django import template

from ..models import Menu, CompanyLogo

register = template.Library()


@register.simple_tag()
def get_menu(slug):
    return Menu.objects.get(slug=slug) 

@register.simple_tag()
def company_logo():
    return CompanyLogo.objects.first()