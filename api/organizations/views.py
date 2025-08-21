from rest_framework import views, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.auth.permissions import IsOrganizationFacilitator, IsOrganizationLearner

from django.shortcuts import get_object_or_404

from .models import Organization, OrganizationCourse, OrganizationLearner, OrganizationFacilitator
from .serializers import OrganizationSerializer, OrganizationCourseSerializer, OrganizationLearnerSerializer, OrganizationFacilitatorSerializer
from api.users.models import Facilitator, Learner

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class OrganizationLearnerViewSet(viewsets.ModelViewSet):
    queryset = OrganizationLearner.objects.all()
    serializer_class = OrganizationLearnerSerializer


class OrganizationFacilitatorViewSet(viewsets.ModelViewSet):
    queryset = OrganizationFacilitator.objects.all()
    serializer_class = OrganizationFacilitatorSerializer


class FacilitatedOrganizationsView(views.APIView):
    def get(self, request):
        user = request.user
        facilitator = get_object_or_404(Facilitator, user=user)
        
        organizations = Organization.objects.filter(
            organization_facilitator__facilitator=facilitator
        )
        
        serializer = OrganizationSerializer(organizations, many=True)

        return Response(serializer.data)
    

class RegisteredOrganizationsView(views.APIView):
    def get(self, request):
        user = request.user
        learner = get_object_or_404(Learner, user=user)
        
        organizations = Organization.objects.filter(
            organization_learner__learner=learner
        )
        
        serializer = OrganizationSerializer(organizations, many=True)

        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        user = request.user
        learner = get_object_or_404(Learner, user=user)
        add_code = request.data.get('add_code')

        if not add_code:
            return Response({"error": "Please enter an add code and try again."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            organization = Organization.objects.get(add_code=add_code)
        except Organization.DoesNotExist:
            return Response({"error": "No organization was found with the given add code. Please verify the add code and try again."}, status=status.HTTP_404_NOT_FOUND)

        current_learners_count = OrganizationLearner.objects.filter(organization=organization).count()
        if current_learners_count >= organization.seats:
            return Response({"error": "This organization has reached the maximum number of learners. Contact the organization's facilitator for more information."}, status=status.HTTP_400_BAD_REQUEST)
        
        if OrganizationLearner.objects.filter(organization=organization, learner=learner).exists():
            return Response({"error": "You are already a member of this organization."}, status=status.HTTP_400_BAD_REQUEST)
        
        organization_learner = OrganizationLearner.objects.create(organization=organization, learner=learner)
        return Response({"detail": "OrganizationLearner record created successfully."}, status=status.HTTP_201_CREATED)
    

class OrganizationCourseView(views.APIView):
    permission_classes = [IsAuthenticated, IsOrganizationFacilitator | IsOrganizationLearner]
    def get(self, request, organization_id):
        organization = Organization.objects.get(id=organization_id)
        self.check_object_permissions(request, organization)
        
        organization_courses = OrganizationCourse.objects.filter(organization_id=organization_id)
        serializer = OrganizationCourseSerializer(organization_courses, context={'request': request}, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    

class OrganizationLearnerView(views.APIView):
    permission_classes = [IsAuthenticated, IsOrganizationFacilitator]
    def get(self, request, organization_id):
        organization = Organization.objects.get(id=organization_id)
        self.check_object_permissions(request, organization)
        
        learners = OrganizationLearner.objects.filter(organization__id=organization_id)
        serializer = OrganizationLearnerSerializer(learners, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)