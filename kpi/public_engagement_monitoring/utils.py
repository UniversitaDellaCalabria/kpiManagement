import requests

from django.conf import settings
from django.core.mail import send_mail

from organizational_area.models import *
from organizational_area.utils import user_in_office

from . settings import *


# def user_is_teacher(matricola='', encrypted=False):
    # if not matricola:
        # return False
    # if not encrypted:
        # response = requests.post(f'{API_ENCRYPTED_ID}',
                                 # data={'id': matricola},
                                 # headers={'Authorization': f'Token {settings.STORAGE_TOKEN}'})
        # if response.status_code == 200:
            # matricola = response.json()
        # else:
            # return False
    # response = requests.get(f"{API_TEACHER_URL}{matricola}")
    # if response.status_code == 200:
        # return True
    # return False


def user_is_operator(user, structure=None):
    return user_in_office(user, [OPERATOR_OFFICE], structure)


def user_is_patronage_operator(user, structure=None):
    return user_in_office(user, [PATRONAGE_OFFICE], structure)


def user_is_manager(user):
    return user_in_office(user, [MANAGER_OFFICE])


def send_email_to_event_referents(event, subject, body):
    recipients = [event.referent.email]
    if event.created_by.email not in recipients:
        recipients.append(event.created_by.email)
    send_mail(
        subject=subject,
        message=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipients,
        fail_silently=True,
    )


def send_email_to_operators(structure, subject, body):
    recipients = OrganizationalStructureOfficeEmployee.objects.filter(employee__is_active=True,
                                                                      office__is_active=True,
                                                                      office__slug=OPERATOR_OFFICE,
                                                                      office__organizational_structure=structure,
                                                                      office__organizational_structure__is_active=True).values_list('employee__email', flat=True)
    send_mail(
        subject=subject,
        message=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipients,
        fail_silently=True,
    )


def send_email_to_patronage_operators(structure, subject, body):
    recipients = OrganizationalStructureOfficeEmployee.objects.filter(employee__is_active=True,
                                                                      office__is_active=True,
                                                                      office__slug=PATRONAGE_OFFICE,
                                                                      office__organizational_structure=structure,
                                                                      office__organizational_structure__is_active=True).values_list('employee__email', flat=True)
    send_mail(
        subject=subject,
        message=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipients,
        fail_silently=True,
    )


def send_email_to_managers(subject, body):
    recipients = OrganizationalStructureOfficeEmployee.objects.filter(employee__is_active=True,
                                                                      office__is_active=True,
                                                                      office__slug=MANAGER_OFFICE,
                                                                      office__organizational_structure__is_active=True).values_list('employee__email', flat=True)
    send_mail(
        subject=subject,
        message=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipients,
        fail_silently=True,
    )
