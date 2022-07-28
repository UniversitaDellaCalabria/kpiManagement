from django.urls import path

from . views import *
from . datatables import *

app_name = 'detection'

# app prefix
prefix = 'enabling-factors'

urlpatterns = [

    path(f'{prefix}/', dashboard, name='dashboard'),

    # datatables
    path(f'{prefix}/<str:structure_slug>/detections.json',
         datatables_structure_detections, name='structure_detections_json'),

    path(f'{prefix}/<str:structure_slug>/',
         structure_detections, name='structure_detections'),
    path(f'{prefix}/<str:structure_slug>/new/',
         new_structure_detection, name='new_structure_detection'),
    path(f'{prefix}/<str:structure_slug>/<str:detection_pk>/',
         structure_detection, name='structure_detection'),
    path(f'{prefix}/<str:structure_slug>/<str:detection_pk>/edit/',
         edit_structure_detection, name='edit_structure_detection'),
]
