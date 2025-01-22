from rest_framework import serializers

from .. models import PublicEngagementEvent


class PublicEngagementEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicEngagementEvent
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['created_by'] = f'{instance.created_by.first_name} {instance.created_by.last_name}'
        if instance.manager_taken_by:
            data['manager_taken_by'] = f'{instance.manager_taken_by.first_name} {instance.manager_taken_by.last_name}'
        data['modified_by'] = f'{instance.modified_by.first_name} {instance.modified_by.last_name}'
        if instance.operator_taken_by:
            data['operator_taken_by'] = f'{instance.operator_taken_by.first_name} {instance.operator_taken_by.last_name}'
        data['referent'] = f'{instance.referent.first_name} {instance.referent.last_name}'
        data['structure'] = f'{instance.structure.name}'
        data['is_ready_for_request_evaluation'] = instance.is_ready_for_request_evaluation()
        data['can_be_taken_by_evaluation_operator'] = instance.can_be_taken_by_evaluation_operator()
        data['can_be_taken_by_patronage_operator'] = instance.can_be_taken_by_patronage_operator()
        data['can_be_taken_by_manager'] = instance.can_be_taken_by_manager()
        data['is_ready_for_evaluation_operator_evaluation'] = instance.is_ready_for_evaluation_operator_evaluation()
        data['is_ready_for_patronage_operator_evaluation'] = instance.is_ready_for_patronage_operator_evaluation()
        data['is_ready_for_manager_evaluation'] = instance.is_ready_for_manager_evaluation()
        data['is_evaluated_positively_by_operator'] = instance.is_evaluated_positively_by_operator()
        data['is_evaluated_negatively_by_operator'] = instance.is_evaluated_negatively_by_operator()
        data['is_evaluated_positively_by_patronage_operator'] = instance.is_evaluated_positively_by_patronage_operator()
        data['is_evaluated_negatively_by_patronage_operator'] = instance.is_evaluated_negatively_by_patronage_operator()
        data['is_evaluated_positively_by_manager'] = instance.is_evaluated_positively_by_manager()
        data['is_evaluated_negatively_by_manager'] = instance.is_evaluated_negatively_by_manager()

        return data
