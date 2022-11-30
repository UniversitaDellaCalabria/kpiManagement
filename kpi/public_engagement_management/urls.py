from django.urls import path

from . datatables import *
from . views import *


app_name = 'public_engagement'


# app prefix
prefix = 'public_engagement'

urlpatterns = [

    path(f'{prefix}/', dashboard, name='dashboard'),

    # datatables
    path(f'{prefix}/<str:structure_slug>/public_engagements.json',
         datatables_structure_public_engagements, name='structure_public_engagements_json'),

    path(f'{prefix}/<str:structure_slug>/',
         structure_public_engagements, name='structure_public_engagements'),
    path(f'{prefix}/<str:structure_slug>/new/',
         structure_public_engagement_new, name='structure_public_engagement_new'),
    path(f'{prefix}/<str:structure_slug>/<str:public_engagement_pk>/',
         structure_public_engagement, name='structure_public_engagement'),
    path(f'{prefix}/<str:structure_slug>/<str:public_engagement_pk>/edit/',
         structure_public_engagement_edit, name='structure_public_engagement_edit'),
    path(f'{prefix}/<str:structure_slug>/<str:public_engagement_pk>/partners/add/',
         structure_public_engagement_partner_add, name='structure_public_engagement_partner_add'),
    path(f'{prefix}/<str:structure_slug>/<str:public_engagement_pk>/partners/<str:partner_pk>/edit/',
         structure_public_engagement_partner_edit, name='structure_public_engagement_partner_edit'),
    path(f'{prefix}/<str:structure_slug>/<str:public_engagement_pk>/partners/<str:partner_pk>/delete/',
         structure_public_engagement_partner_delete, name='structure_public_engagement_partner_delete'),
]
