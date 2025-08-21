from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'attempts', views.QuizAttemptViewSet, basename='quiz_attempts')

urlpatterns = [
    path('', include(router.urls)),
    path('organization/<int:organization_id>/learner/<int:learner_id>', views.QuizListView.as_view(), name='learner_quiz_details'),
    path('organization/<int:organization_id>/learner/<int:learner_id>/attempts/<int:attempt_id>', views.QuizAttemptFacilitatorView.as_view(), name='learner_quiz_details'),
    path('<int:course_id>', views.QuizDetailsView.as_view(), name='learner_quiz_details'),
    path('<int:course_id>/details', views.UnprotectedQuizDetailsView.as_view(), name='learner_quiz_details'),
    path('courses/<int:course_id>/attempts/', views.QuizAttemptView.as_view(), name='learner_quiz_attempts'),
    path('attempts/<int:attempt_id>/grade/', views.QuizGradeView.as_view(), name='grade_quiz'),
    path('attempts/<int:attempt_id>/questions/<int:question_id>/answer/', views.QuizQuestionCompletionView.as_view(), name='answer_question'),
    path('create/', views.CreateQuiz.as_view(), name='create_quiz'),
]