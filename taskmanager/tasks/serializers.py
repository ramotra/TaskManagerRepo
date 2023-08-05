from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Task
        fields = '__all__'
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super(TaskSerializer, self).create(validated_data)