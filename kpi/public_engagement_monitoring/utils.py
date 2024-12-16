import requests

from django.conf import settings

from . settings import API_ENCRYPTED_ID, API_TEACHER_URL


def user_is_teacher(matricola='', encrypted=False):
    if not matricola: return False
    if not encrypted:
        response = requests.post(f'{API_ENCRYPTED_ID}',
                                 data={'id': matricola},
                                 headers={'Authorization': f'Token {settings.STORAGE_TOKEN}'})
        if response.status_code == 200:
            matricola = response.json()
        else:
            return False
    response = requests.get(f"{API_TEACHER_URL}{matricola}")
    if response.status_code == 200:
        return True
    return False
