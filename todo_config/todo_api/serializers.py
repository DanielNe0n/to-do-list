from rest_framework import serializers
from ToDoList.models import Task


class TaskSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%H:%M %Y-%m-%d", read_only=True)
    updated_at = serializers.DateTimeField(format="%H:%M %Y-%m-%d", read_only=True)
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = Task
        fields = '__all__'