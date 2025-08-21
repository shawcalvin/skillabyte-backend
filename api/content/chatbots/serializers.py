from rest_framework import serializers
from .models import Prompt, Conversation

class PromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prompt
        fields = ['id', 'course', 'prompt', 'feedback_prompt']
        read_only_fields = ['id']

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = [
            'id', 
            'prompt', 
            'messages', 
            'feedback', 
            'model', 
            'attempt'
        ]
        read_only_fields = ['id']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['messages'] = [
            message for message in representation['messages']
            if message.get('role') != 'system'
        ]
        
        return representation