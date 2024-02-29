from django import template

from liberty.models import ItemLike

register = template.Library()



def check_like(item, user):
    return ItemLike.objects.filter(item=item, user=user).exists()
register.filter(check_like)