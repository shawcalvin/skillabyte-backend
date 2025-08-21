from django.db.models.signals import post_save
from django.dispatch import receiver

from api.users.models import User, Learner, Facilitator
from .models import Organization, OrganizationLearner, OrganizationFacilitator

@receiver(post_save, sender=User)
def create_personal_organization(sender, instance, created, **kwargs):
    """
    Signal handler to create a personal organization instance whenever a new user is created.
    """
    if created:
        user: User = instance
        organization = Organization.objects.create(
            name=f'My Purchased Courses', 
            description=f'Personal organization for {user.first_name} {user.last_name}',
            is_personal=True
        )
        learner = Learner.objects.create(user=user)
        facilitator = Facilitator.objects.create(user=user)
        OrganizationLearner.objects.create(organization=organization, learner=learner)
        OrganizationFacilitator.objects.create(organization=organization, facilitator=facilitator)
