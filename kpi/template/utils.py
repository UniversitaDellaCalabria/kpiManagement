import datetime

from django.shortcuts import render
from django.utils import timezone


def get_datetime_delta(days):
    delta_date = timezone.now() - datetime.timedelta(days=days)
    return delta_date.replace(hour=0, minute=0, second=0)


def custom_message(request, message='', status=None):
    """
    """
    return render(request, 'custom_message.html',
                  {'avviso': message},
                  status=status)
