import datetime

from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
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


def log_action(user, obj, flag, msg):
    LogEntry.objects.log_action(user_id=user.pk,
                                content_type_id=ContentType.objects.get_for_model(
                                    obj).pk,
                                object_id=obj.pk,
                                object_repr=obj.__str__(),
                                action_flag=flag,
                                change_message=msg)


def check_user_permission_on_object(user, obj, permission='view'):
    # check for locks on object
    content_type = ContentType.objects.get_for_model(obj)
    app_name = content_type.__dict__['app_label']
    model = content_type.__dict__['model']

    # get Django permissions on object
    return user.has_perm(f'{app_name}.{permission}_{model}')
