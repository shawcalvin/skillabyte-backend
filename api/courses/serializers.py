from rest_framework import serializers
from .models import Course, LearningObjective, FieldOfStudy, KnowledgeLevel, Tag

class CourseSerializer(serializers.ModelSerializer):
    learning_objectives = serializers.SerializerMethodField()
    prerequisite_courses = serializers.SerializerMethodField()
    fields_of_study = serializers.SerializerMethodField()
    knowledge_level = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id',
            'title', 
            'description',
            'overview', 
            'knowledge_level', 
            'fields_of_study', 
            'cpe_credits', 
            'learning_objectives',
            'prerequisite_courses', 
            'prerequisite_knowledge',
            'advance_preparation',
            'tags',
            'created_at',
            'reviewed_at'
        ]

    def get_learning_objectives(self, obj):
        objects = LearningObjective.objects.filter(course=obj)
        return LearningObjectiveSerializer(objects, many=True).data
    
    def get_prerequisite_courses(self, obj):
        objects = obj.prerequisite_courses.all()
        return PrerequisiteCourseSerializer(objects, many=True).data
    
    def get_fields_of_study(self, obj):
        objects = obj.fields_of_study.all()
        return FieldOfStudySerializer(objects, many=True).data
    
    def get_knowledge_level(self, obj):
        objects = obj.knowledge_level
        return KnowledgeLevelSerializer(objects).data
    
    def get_tags(self, obj):
        objects = obj.tags.all()
        return TagSerializer(objects, many=True).data
    

class PrerequisiteCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title']


class LearningObjectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningObjective
        fields = ['objective']


class FieldOfStudySerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldOfStudy
        fields = ['name']


class KnowledgeLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnowledgeLevel
        fields = ['name']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']