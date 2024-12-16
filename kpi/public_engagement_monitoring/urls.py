from django.urls import path

from . views import *


app_name = 'public_engagement_monitoring'


# app prefix
prefix = 'public-engagement-monitoring'

user_prefix = 'user'
operator_prefix = 'operator'
manager_prefix = 'manager'

urlpatterns = [
    path(f'{prefix}/', dashboard, name='dashboard'),

    # user
    path(f'{prefix}/{user_prefix}/', user_dashboard, name='user_dashboard'),
    path(f'{prefix}/{user_prefix}/new/', new, name='new'),
    path(f'{prefix}/{user_prefix}/new/step-1/', new_step_1, name='new_step_1'),
    path(f'{prefix}/{user_prefix}/<int:event_id>/', event, name='event'),
    path(f'{prefix}/{user_prefix}/<int:event_id>/fase1/', event_fase1, name='event_fase1'),

    # operator
    # path(f'{prefix}/{operator_prefix}/', operator_dashboard, name='operator_dashboard'),
]
