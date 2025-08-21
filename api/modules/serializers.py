from rest_framework import serializers
from .models import LearningModule, LearningModuleAttempt, LearningModuleCompletion
from api.courses.serializers import CourseSerializer

class LearningModuleSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    class Meta:
        model = LearningModule
        fields = ['id', 'course', 'module_path']

class LearningModuleAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningModuleAttempt
        fields = ['id', 'module', 'learner', 'date_started', 'date_submitted']


class LearningModuleCompletionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningModuleCompletion
        fields = ['id', 'attempt', 'page_number', 'time_spent']
