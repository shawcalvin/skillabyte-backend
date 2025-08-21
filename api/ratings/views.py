from django.shortcuts import get_object_or_404

from rest_framework import views, status
from rest_framework.response import Response

from .models import RatingCategory
from .serializers import RatingCategorySerializer, CourseRatingSerializer
from .services import RatingsService
from api.courses.models import Course

class CourseRatingCategoriesView(views.APIView):
    def get(self, request):
        categories = RatingCategory.objects.all()
        serializer = RatingCategorySerializer(categories, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CourseRatingView(views.APIView):
    def post(self, request, course_id):
        ratings_service = RatingsService()
        learner = request.user.learner_profile

        entries_data = request.data.get('entries', [])
        rating = ratings_service.create_rating(
            course_id=course_id,
            learner_id=learner.pk,
            comments = request.data.get('comments')
        )

        for entry in entries_data:
            category_id = entry['category_id']
            score = entry['score']

            try:
                ratings_service.create_entry(rating.pk, category_id, score)
            except Exception as e:
                rating.delete()
                return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
        serializer = CourseRatingSerializer(rating)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

