from django import template

register = template.Library()

@register.filter
def is_author_or_superuser(user, author_username):
    return user.is_superuser or user.username == author_username