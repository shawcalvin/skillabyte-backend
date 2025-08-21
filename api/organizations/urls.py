from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'learners', views.OrganizationLearnerViewSet, basename='organization_learners')
router.register(r'facilitators', views.OrganizationFacilitatorViewSet, basename='organization_facilitators')
router.register(r'organizations', views.OrganizationViewSet, basename='organizations')

urlpatterns = [
    path('', include(router.urls)),
    path('facilitated/', views.FacilitatedOrganizationsView.as_view(), name='facilitated_organizations'),
    path('registered/', views.RegisteredOrganizationsView.as_view(), name='facilitated_organizations'),
    path('<int:organization_id>/courses/', views.OrganizationCourseView.as_view(), name='organization_courses'),
    path('<int:organization_id>/learners/', views.OrganizationLearnerView.as_view(), name='organization_learners'),
]