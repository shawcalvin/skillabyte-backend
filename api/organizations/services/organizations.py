from datetime import timedelta
from django.utils import timezone

from ..models import Organization, OrganizationCourse

class OrganizationService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(OrganizationService, cls).__new__(cls)
        return cls._instance
    
    def get_personal_organization(self, user):
        return Organization.objects.filter(
            organization_facilitator__facilitator=user.facilitator_profile,
            is_personal=True
        ).first()
    
    def add_course_to_organization(self, organization, course):
        return OrganizationCourse.objects.create(
        organization=organization,
        course=course,
        expires=timezone.now() + timedelta(days=365)
    )