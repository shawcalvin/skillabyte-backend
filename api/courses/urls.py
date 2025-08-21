from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'courses', views.CourseViewSet, basename='courses')

urlpatterns = [
    path('', include(router.urls)),
    path('registered/', views.RegisteredCoursesView.as_view(), name='registered_courses'),
    path('completed/', views.CompletedCoursesView.as_view(), name='completed_courses')
]