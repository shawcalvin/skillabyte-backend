from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404

from .models import Course
from .serializers import CourseSerializer
from api.users.models import Learner
from api.organizations.models import OrganizationCourse, OrganizationLearner
from api.organizations.serializers import OrganizationCourseSerializer
from api.content.quizzes.models import QuizAttempt

class CourseViewSet(viewsets.ModelViewSet):
    permission_classes=[AllowAny]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    
class RegisteredCoursesView(APIView):
    def get(self, request):
        user = request.user
        learner = get_object_or_404(Learner, user=user)
        
        organization_courses = OrganizationCourse.objects.filter(
            organization__organization_learner__learner=learner
        ).select_related('course', 'organization')
        
        serializer = OrganizationCourseSerializer(organization_courses, many=True)

        return Response(serializer.data)
    

class CompletedCoursesView(APIView):
    def get(self, request):
        user = request.user
        learner = get_object_or_404(Learner, user=user)

        registered_course_ids = (
            OrganizationLearner.objects.filter(learner=learner)
            .exclude(organization__organization_course__course__isnull=True)
            .values_list('organization__organization_course__course', flat=True)
            .distinct()
        )

        completed_courses = []

        # Iterate through the registered courses
        for course_id in registered_course_ids:
            course = Course.objects.get(id=course_id)

            # Get all passing quiz attempts (score >= 70%) for the learner and course
            passing_attempts = (
                QuizAttempt.objects.filter(learner=learner, quiz__course=course, score__gte=70.0)
                .order_by('time_submitted')  # Order by the earliest submission date
            )

            # If there are any passing attempts, use the earliest one
            if passing_attempts.exists():
                earliest_attempt = passing_attempts.first()
                completed_course_data = {
                    "course": CourseSerializer(course).data,
                    "completed_date": earliest_attempt.time_submitted,
                }
                completed_courses.append(completed_course_data)

        return Response(completed_courses, status=status.HTTP_200_OK)