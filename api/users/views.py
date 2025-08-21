from rest_framework import views, viewsets, status
from rest_framework.response import Response

from .models import Learner, User
from .serializers import LearnerSerializer, UserSerializer

class LearnerViewSet(viewsets.ModelViewSet):
    queryset = Learner.objects.all()
    serializer_class = LearnerSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer