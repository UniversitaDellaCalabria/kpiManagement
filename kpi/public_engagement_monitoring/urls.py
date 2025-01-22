from django.urls import path

from . api.views import (user as api_user,
                         operator as api_evaluation_operator,
                         patronage as api_patronage_operator,
                         manager as api_manager)
from . views import generic, manager, operator, patronage, user


app_name = 'public_engagement_monitoring'


# app prefix
prefix = 'public-engagement-monitoring'

api_prefix = "api"
user_prefix = 'user'
operator_prefix = 'operator'
validator_prefix = 'evaluation'
patronage_prefix = 'patronage'
manager_prefix = 'manager'

urlpatterns = [
    path(f'{prefix}/', generic.dashboard, name='dashboard'),

    # user
    path(f'{prefix}/{user_prefix}/events/', user.events, name='user_events'),
    path(f'{prefix}/{user_prefix}/events/new/',
         user.new_event_choose_referent, name='user_new_event_choose_referent'),
    path(f'{prefix}/{user_prefix}/events/new/basic-info/',
         user.new_event_basic_info, name='user_new_event_basic_info'),
    path(f'{prefix}/{user_prefix}/events/<int:event_id>/',
         user.event, name='user_event'),
    path(f'{prefix}/{user_prefix}/events/<int:event_id>/basic-info/',
         user.event_basic_info, name='user_event_basic_info'),
    path(f'{prefix}/{user_prefix}/events/<int:event_id>/data/',
         user.event_data, name='user_event_data'),
    path(f'{prefix}/{user_prefix}/events/<int:event_id>/report/',
         user.event_report, name='user_event_report'),
    path(f'{prefix}/{user_prefix}/events/<int:event_id>/people/',
         user.event_people, name='user_event_people'),
    path(f'{prefix}/{user_prefix}/events/<int:event_id>/people/delete/<int:person_id>/',
         user.event_people_delete, name='user_event_people_delete'),
    path(f'{prefix}/{user_prefix}/events/<int:event_id>/request-evaluation/',
         user.event_request_evaluation, name='user_event_request_evaluation'),
    path(f'{prefix}/{user_prefix}/events/<int:event_id>/request-evaluation-cancel/',
         user.event_request_evaluation_cancel, name='user_event_request_evaluation_cancel'),
    path(f'{prefix}/{user_prefix}/events/<int:event_id>/clone/',
         user.event_clone, name='user_event_clone'),
    path(f'{prefix}/{user_prefix}/events/<int:event_id>/delete/',
         user.event_delete, name='user_event_delete'),

    # evaluation operator
    path(f'{prefix}/{operator_prefix}/{validator_prefix}/',
         operator.dashboard, name='operator_dashboard'),
    path(f'{prefix}/{operator_prefix}/{validator_prefix}/<str:structure_slug>/events/',
         operator.events, name='operator_events'),
    path(f'{prefix}/{operator_prefix}/{validator_prefix}/<str:structure_slug>/events/new/',
         operator.new_event_choose_referent, name='operator_new_event_choose_referent'),
    path(f'{prefix}/{operator_prefix}/{validator_prefix}/<str:structure_slug>/events/new/basic-info/',
         operator.new_event_basic_info, name='operator_new_event_basic_info'),
    path(f'{prefix}/{operator_prefix}/{validator_prefix}/<str:structure_slug>/events/<int:event_id>/',
         operator.event, name='operator_event'),
    path(f'{prefix}/{operator_prefix}/{validator_prefix}/<str:structure_slug>/events/<int:event_id>/take/',
         operator.take_event, name='operator_take_event'),
    path(f'{prefix}/{operator_prefix}/{validator_prefix}/<str:structure_slug>/events/<int:event_id>/basic-info/',
         operator.event_basic_info, name='operator_event_basic_info'),
    path(f'{prefix}/{operator_prefix}/{validator_prefix}/<str:structure_slug>/events/<int:event_id>/data/',
         operator.event_data, name='operator_event_data'),
    path(f'{prefix}/{operator_prefix}/{validator_prefix}/<str:structure_slug>/events/<int:event_id>/people/',
         operator.event_people, name='operator_event_people'),
    path(f'{prefix}/{operator_prefix}/{validator_prefix}/<str:structure_slug>/events/<int:event_id>/people/delete/<int:person_id>/',
         operator.event_people_delete, name='operator_event_people_delete'),
    path(f'{prefix}/{operator_prefix}/{validator_prefix}/<str:structure_slug>/events/<int:event_id>/evaluate/',
         operator.event_evaluation, name='operator_event_evaluation'),
    path(f'{prefix}/{operator_prefix}/{validator_prefix}/<str:structure_slug>/events/<int:event_id>/reopen-evaluation/',
         operator.event_reopen_evaluation, name='operator_event_reopen_evaluation'),

    # patronage operator
    path(f'{prefix}/{operator_prefix}/{patronage_prefix}/',
         patronage.dashboard, name='patronage_operator_dashboard'),
    path(f'{prefix}/{operator_prefix}/{patronage_prefix}/<str:structure_slug>/events/',
         patronage.events, name='patronage_operator_events'),
    path(f'{prefix}/{operator_prefix}/{patronage_prefix}/<str:structure_slug>/events/<int:event_id>/',
         patronage.event, name='patronage_operator_event'),
    path(f'{prefix}/{operator_prefix}/{patronage_prefix}/<str:structure_slug>/events/<int:event_id>/take/',
         patronage.take_event, name='patronage_operator_take_event'),
    path(f'{prefix}/{operator_prefix}/{patronage_prefix}/<str:structure_slug>/events/<int:event_id>/evaluate/',
         patronage.event_evaluation, name='patronage_operator_event_evaluation'),
    path(f'{prefix}/{operator_prefix}/{patronage_prefix}/<str:structure_slug>/events/<int:event_id>/reopen-evaluation/',
         patronage.event_reopen_evaluation, name='patronage_operator_event_reopen_evaluation'),

    # manager
    path(f'{prefix}/{manager_prefix}/',
         manager.dashboard, name='manager_dashboard'),
    path(f'{prefix}/{manager_prefix}/<str:structure_slug>/events/',
         manager.events, name='manager_events'),
    path(f'{prefix}/{manager_prefix}/<str:structure_slug>/events/new/',
         manager.new_event_choose_referent, name='manager_new_event_choose_referent'),
    path(f'{prefix}/{manager_prefix}/<str:structure_slug>/events/new/basic-info/',
         manager.new_event_basic_info, name='manager_new_event_basic_info'),
    path(f'{prefix}/{manager_prefix}/<str:structure_slug>/events/<int:event_id>/',
         manager.event, name='manager_event'),
    path(f'{prefix}/{manager_prefix}/<str:structure_slug>/events/<int:event_id>/take/',
         manager.take_event, name='manager_take_event'),
    path(f'{prefix}/{manager_prefix}/<str:structure_slug>/events/<int:event_id>/basic-info/',
         manager.event_basic_info, name='manager_event_basic_info'),
    path(f'{prefix}/{manager_prefix}/<str:structure_slug>/events/<int:event_id>/data/',
         manager.event_data, name='manager_event_data'),
    path(f'{prefix}/{manager_prefix}/<str:structure_slug>/events/<int:event_id>/people/',
         manager.event_people, name='manager_event_people'),
    path(f'{prefix}/{manager_prefix}/<str:structure_slug>/events/<int:event_id>/people/delete/<int:person_id>/',
         manager.event_people_delete, name='manager_event_people_delete'),
    path(f'{prefix}/{manager_prefix}/<str:structure_slug>/events/<int:event_id>/evaluate/',
         manager.event_evaluation, name='manager_event_evaluation'),
    path(f'{prefix}/{manager_prefix}/<str:structure_slug>/events/<int:event_id>/reopen-evaluation/',
         manager.event_reopen_evaluation, name='manager_event_reopen_evaluation'),

    # API
    path(f'{prefix}/{api_prefix}/{user_prefix}/events/',
         api_user.PublicEngagementEventList.as_view(), name='api_user_events'),
    path(f'{prefix}/{api_prefix}/{operator_prefix}/{validator_prefix}/<str:structure_slug>/events/',
         api_evaluation_operator.PublicEngagementEventList.as_view(), name='api_evaluation_operator_events'),
    path(f'{prefix}/{api_prefix}/{operator_prefix}/{patronage_prefix}/<str:structure_slug>/events/',
         api_patronage_operator.PublicEngagementEventList.as_view(), name='api_patronage_operator_events'),
    path(f'{prefix}/{api_prefix}/{manager_prefix}/<str:structure_slug>/events/',
         api_manager.PublicEngagementEventList.as_view(), name='api_manager_events'),
]
