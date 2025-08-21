from django.db import models
from django.contrib.postgres.fields import ArrayField

from api.modules.models import LearningModuleAttempt
from api.courses.models import Course

class Prompt(models.Model):
    prompt = models.TextField(null=False)
    feedback_prompt = models.TextField()


class Conversation(models.Model):
    prompt = models.ForeignKey(Prompt, null=False, on_delete=models.PROTECT)
    messages = ArrayField(models.JSONField())
    feedback = models.TextField(null=True)
    model = models.TextField(default="chatgpt-4o-latest")
    attempt = models.ForeignKey(LearningModuleAttempt, null=False, on_delete=models.CASCADE)


class PromptIndex(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE)
    index = models.IntegerField()