from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api.organizations.models import OrganizationFacilitator

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'open_to_research']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'open_to_research': {'required': True},
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        try:
            user = User.objects.create_user(
                email=validated_data['email'],
                password=validated_data['password'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                open_to_research = validated_data['open_to_research']
            )
            return user
        
        except IntegrityError as e:
            raise ValidationError({"email": "An account with this email already exists."})


class LoginSerializer(TokenObtainPairSerializer):  
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['id'] = str(user.id)
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['email'] = user.email
        token['is_facilitator'] = not user.facilitator_profile.is_personal

        return token