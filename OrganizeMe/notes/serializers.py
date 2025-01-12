from .models import Note
from rest_framework import serializers


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'  # Include all fields of the Note model
        read_only_fields = ['user']  # Prevent 'user' from being required in requests

    def create(self, validated_data):
        # Automatically associate the note with the logged-in user
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Ensure the user cannot be updated
        validated_data.pop('user', None)
        return super().update(instance, validated_data)
