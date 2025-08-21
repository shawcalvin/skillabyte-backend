from django.utils import timezone

from rest_framework import views, viewsets, status
from rest_framework.response import Response

from .models import LearningModule, LearningModuleAttempt, LearningModuleCompletion
from .serializers import LearningModuleSerializer, LearningModuleAttemptSerializer, LearningModuleCompletionSerializer
from api.users.models import Learner

class LearningModuleView(views.APIView):
    def get(self, request, course_id, *args, **kwargs):
        try:
            module = LearningModule.objects.get(course_id=course_id)
        except LearningModule.DoesNotExist:
            return Response({"error": "No learning module found for given course"}, status=status.HTTP_404_NOT_FOUND)

        serializer = LearningModuleSerializer(module)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LearningModuleAttemptView(views.APIView):
    def get(self, request, course_id, *args, **kwargs):
        attempts = LearningModuleAttempt.objects.filter(module__course_id=course_id, learner__user=request.user)
        serializer = LearningModuleAttemptSerializer(attempts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, course_id, *args, **kwargs):
        module = LearningModule.objects.get(course_id=course_id)
        learner = Learner.objects.get(user=request.user)

        attempt = LearningModuleAttempt.objects.create(module=module, learner=learner)
        serializer = LearningModuleAttemptSerializer(attempt)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LearningModuleCompletionView(views.APIView):
    def get(self, request, attempt_id, *args, **kwargs):
        try:
            attempt = LearningModuleAttempt.objects.get(id=attempt_id)
        except LearningModuleAttempt.DoesNotExist:
            return Response({"error": "No attempt found with given id."}, status=status.HTTP_404_NOT_FOUND)
        
        page_completions = LearningModuleCompletion.objects.filter(attempt=attempt)
        serializer = LearningModuleCompletionSerializer(page_completions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, attempt_id, *args, **kwargs):
        page_number = request.data.get('page_number')
        time_spent = request.data.get('time_spent')

        if page_number is None or time_spent is None:
            return Response({"error": "'page_number' and 'time_spent' fields are required."}, status=status.HTTP_400_BAD_REQUEST )

        page_completion, created = LearningModuleCompletion.objects.get_or_create(
            attempt_id=attempt_id,
            page_number=page_number,
            defaults={'time_spent': time_spent}
        )

        if not created:
            page_completion.time_spent += time_spent
            page_completion.save()

        serializer = LearningModuleCompletionSerializer(page_completion)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LearningModuleSubmissionView(views.APIView):
    def post(self, request, attempt_id, *args, **kwargs):
        try:
            attempt = LearningModuleAttempt.objects.get(id=attempt_id)
        except LearningModuleAttempt.DoesNotExist:
            return Response({"error": "No attempt found with given id."}, status=status.HTTP_404_NOT_FOUND)

        attempt.date_submitted = timezone.now()
        attempt.save()
        
        return Response({"message": "Attempt submitted."}, status=status.HTTP_200_OK)
        
