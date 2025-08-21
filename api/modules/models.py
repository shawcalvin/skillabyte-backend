from django.db import models

from api.users.models import Learner
from api.courses.models import Course

class LearningModule(models.Model):
    course = models.OneToOneField(Course, null=False, on_delete=models.CASCADE)
    module_path = models.TextField()


class LearningModuleAttempt(models.Model):
    module = models.ForeignKey(LearningModule, null=False, on_delete=models.PROTECT)
    learner = models.ForeignKey(Learner, null=False, on_delete=models.CASCADE)
    date_started = models.DateTimeField(auto_now_add=True)
    date_submitted = models.DateTimeField(null=True, default=None)


class LearningModuleCompletion(models.Model):
    attempt = models.ForeignKey(LearningModuleAttempt, null=False, on_delete=models.CASCADE)
    page_number = models.IntegerField(default=0)
    time_spent = models.FloatField(null=False, default=0)