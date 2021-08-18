from datetime import timedelta, datetime

from django import template
from django.utils.timezone import now

from ..models import Task, Category
from time import gmtime, strftime

register = template.Library()


def seconds_to_daytime(seconds):
    days = seconds // 86400
    seconds -= days * 86400
    hours = seconds // 3600
    seconds -= hours * 3600
    minutes = seconds // 60
    seconds -= minutes * 60
    return days, hours, minutes, seconds


@register.simple_tag(name='due_date')
def due_date(time):
    left = time - now()
    seconds = int(left.total_seconds())
    if seconds > 0:
        return '%d days ,%02d hours,%02d minutes,%20d seconds' \
               % (seconds_to_daytime(seconds))
    return 'Due date has passed'
