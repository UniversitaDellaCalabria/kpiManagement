from django.conf import settings


API_TEACHER_URL = getattr(settings, 'API_TEACHER_URL', 'https://storage.portale.unical.it/api/ricerca/teachers/')
API_ADDRESSBOOK_FULL = getattr(settings, 'API_ADDRESSBOOK_FULL', 'https://storage.portale.unical.it/api/ricerca/addressbook-full/')
API_DECRYPTED_ID = getattr(settings, 'API_DECRYPTED_ID', 'https://storage.portale.unical.it/api/ricerca/get-decrypted-person-id/')
API_ENCRYPTED_ID = getattr(settings, 'API_ENCRYPTED_ID', 'https://storage.portale.unical.it/api/ricerca/get-person-id/')

VALIDATOR_INTERMIDIATE = getattr(settings, 'VALIDATOR_INTERMIDIATE', 'public-engagement-intermediate')
VALIDATOR_FINAL = getattr(settings, 'VALIDATOR_FINAL', 'public-engagement-final')
