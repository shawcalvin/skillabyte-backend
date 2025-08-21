from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [
    path('categories/', views.CourseRatingCategoriesView.as_view(), name='rating_categories'),
    path('courses/<int:course_id>/submit/', views.CourseRatingView.as_view(), name='rating_submission'),
]