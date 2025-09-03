from rest_framework import serializers
from todo.models import Todo

class TodoSerializer(serializers.ModelSerializer):
    created = serializers.ReadOnlyField()
    completed = serializers.ReadOnlyField()

    class Meta:
        model = Todo
        fields = ['id', 'title', 'memo', 'created', 'completed']

class TodoToggleCompleteSerializer(serializers.ModelSerializer):
    """
    Serializer para el endpoint de toggle. No recibe campos de entrada;
    solo devuelve el estado actualizado.
    """
    class Meta:
        model = Todo
        fields = ['id', 'completed']
        read_only_fields = ['id', 'completed']