from rest_framework import serializers
from .models import User, Learner, Facilitator, Admin

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'uuid', 'date_joined']


class LearnerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Learner
        fields = ['id', 'user']


class FacilitatorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Facilitator
        fields = ['id', 'user']

class AdminSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Admin
        fields = ['id', 'user']