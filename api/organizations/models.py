import secrets

from django.db import models

from api.courses.models import Course
from api.users.models import Learner, Facilitator

class Organization(models.Model):
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    add_code = models.CharField(max_length=24, unique=True)
    is_personal = models.BooleanField(null=False, default=False)
    seats = models.IntegerField(null=False, default=1)

    def save(self, *args, **kwargs):
        if not self.add_code:
            self.add_code = self.generate_add_code()
        
        super().save(*args, **kwargs)
        

    def generate_add_code(self):
        """
        Generate a unique add code for the organization.
        """
        while True:
            code = secrets.token_hex(12)
            if not Organization.objects.filter(add_code=code).exists():
                return code


class OrganizationCourse(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='organization_course')
    date_added = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    expires = models.DateTimeField(null=False)

    def get_learner_progress(self, learner_id):
        return 0


class OrganizationLearner(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='organization_learner')
    date_added = models.DateTimeField(auto_now_add=True)
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE)


class OrganizationFacilitator(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='organization_facilitator')
    date_added = models.DateTimeField(auto_now_add=True)
    facilitator = models.ForeignKey(Facilitator, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.organization.is_personal:
            if OrganizationFacilitator.objects.filter(organization=self.organization).exists():
                raise ValueError("A personal organization can only have one facilitator.")
        
        super().save(*args, **kwargs)