from django.urls import path

from . datatables import *
from . views import *


app_name = 'visiting'


# app prefix
prefix = 'visiting'

urlpatterns = [

    path(f'{prefix}/', dashboard, name='dashboard'),

    # datatables
    path(f'{prefix}/<str:structure_slug>/visitings.json',
         datatables_structure_visitings, name='structure_visitings_json'),

    path(f'{prefix}/<str:structure_slug>/',
         structure_visitings, name='structure_visitings'),
    path(f'{prefix}/<str:structure_slug>/new/',
         new_structure_visiting, name='new_structure_visiting'),
    path(f'{prefix}/<str:structure_slug>/<str:visiting_pk>/',
         structure_visiting, name='structure_visiting'),
    path(f'{prefix}/<str:structure_slug>/<str:visiting_pk>/edit/',
         edit_structure_visiting, name='edit_structure_visiting'),
]
