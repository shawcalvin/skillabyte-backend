from rest_framework import serializers

from .models import Organization, OrganizationCourse, OrganizationFacilitator, OrganizationLearner
from api.courses.serializers import CourseSerializer
from api.users.serializers import LearnerSerializer, FacilitatorSerializer

class OrganizationSerializer(serializers.ModelSerializer):
    used_seats = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = ['id', 'name', 'description', 'date_created', 'add_code', 'seats', 'used_seats', 'is_personal']

    def get_used_seats(self, obj):
        return OrganizationLearner.objects.filter(organization=obj).count()


class OrganizationCourseSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer()
    course = CourseSerializer()
    amount_completed = serializers.SerializerMethodField()

    class Meta:
        model = OrganizationCourse
        fields = ['id', 'organization', 'date_added', 'expires', 'course', 'amount_completed']

    def get_amount_completed(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
            return obj.get_learner_progress(user.learner_profile.id)
        return None

class OrganizationLearnerSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer()
    learner = LearnerSerializer()
    class Meta:
        model = OrganizationLearner
        fields = ['id', 'organization', 'date_added', 'learner']


class OrganizationFacilitatorSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer()
    facilitator = FacilitatorSerializer()
    class Meta:
        model = OrganizationFacilitator
        fields = ['id', 'organization', 'date_added', 'facilitator']
