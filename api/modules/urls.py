from django.urls import path
from . import views

urlpatterns = [
    path('courses/<int:course_id>/modules/', views.LearningModuleView.as_view(), name="learning_module"),
    path('courses/<int:course_id>/attempts/', views.LearningModuleAttemptView.as_view(), name="learning_module_attempts"),
    path('attempts/<int:attempt_id>/completions/', views.LearningModuleCompletionView.as_view(), name="learing_module_completions"),
    path('attempts/<int:attempt_id>/submit/', views.LearningModuleSubmissionView.as_view(), name="learning_module_submit"),
]