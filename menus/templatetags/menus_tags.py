from django import template

from ..models import Menu, CompanyLogo, BackgroundMenuImage

register = template.Library()


@register.simple_tag()
def get_menu(slug):
    return Menu.objects.get(slug=slug) 

@register.simple_tag()
def company_logo():
    return CompanyLogo.objects.first()

@register.simple_tag()
def background_image():
    return BackgroundMenuImage.objects.first()