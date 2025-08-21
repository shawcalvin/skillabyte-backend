from rest_framework import permissions
from rest_framework import status
from api.organizations.models import Organization, OrganizationFacilitator, OrganizationLearner

class IsOrganizationFacilitator(permissions.BasePermission):
    """
    Custom permission to only allow an organization's facilitators to access an organization object.
    """
    def has_object_permission(self, request, view, obj):
        return obj.organization_facilitator.filter(facilitator__user=request.user).exists()
    

class IsOrganizationLearner(permissions.BasePermission):
    """
    Custom permission to only allow an organization's learners to access an organization object.
    """
    def has_object_permission(self, request, view, obj):
        return obj.organization_learner.filter(learner__user=request.user).exists()
    
class IsAttemptOwnerOrOrgFacilitator(permissions.BasePermission):
    """
    Allow if the requester owns the QuizAttempt OR is a facilitator of the
    attempt's organization. Accepts either a QuizAttempt or Organization object.
    """

    def has_object_permission(self, request, view, obj):
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            return False

        if hasattr(obj, "organization_facilitator"):
            return obj.organization_facilitator.filter(facilitator__user=user).exists()

        attempt = obj
        if getattr(attempt, "learner", None) and getattr(attempt.learner, "user_id", None) == user.id:
            return True

        try:
            organization = attempt.quiz.course.organization
        except Exception:
            organization = getattr(attempt, "organization", None)

        if organization is None:
            return False

        return organization.organization_facilitator.filter(facilitator__user=user).exists()