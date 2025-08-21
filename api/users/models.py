import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError('The email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
 
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
 
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
 
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    uuid = models.UUIDField(
        db_index=True,
        default=uuid.uuid4,
        editable=False
    )
    open_to_research = models.BooleanField(null=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Profile(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Learner(Profile):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='learner_profile')


class Facilitator(Profile):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='facilitator_profile')
    is_personal = models.BooleanField(default=True, null=False)
    

class Admin(Profile):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')