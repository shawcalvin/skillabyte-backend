from rest_framework import serializers
from .models import RatingCategory, CourseRating, CourseRatingEntry

class RatingCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingCategory
        fields = ['id', 'title', 'prompt', 'date_created']


class CourseRatingEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseRatingEntry
        fields = ['category', 'score']


class CourseRatingSerializer(serializers.ModelSerializer):
    entries = CourseRatingEntrySerializer(many=True)

    class Meta:
        model = CourseRating
        fields = ['course', 'learner', 'entries']