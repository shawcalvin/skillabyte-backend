from django.db import models

from api.courses.models import Course, LearningObjective
from api.users.models import Learner

class Quiz(models.Model):
    course = models.ForeignKey(Course, null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, null=False, on_delete=models.CASCADE)
    question = models.TextField()
    question_num = models.IntegerField(null=True)

    class Meta:
        unique_together = ('quiz', 'question_num')


class AnswerChoice(models.Model):
    question = models.ForeignKey(Question, null=False, on_delete=models.CASCADE)
    answer = models.TextField()
    answer_num = models.IntegerField(null=True)
    is_correct = models.BooleanField(null=False)
    feedback = models.TextField(null=False)

    class Meta:
        unique_together = ('question', 'answer_num')


class QuizAttempt(models.Model):
    learner = models.ForeignKey(Learner, null=False, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, null=False, on_delete=models.CASCADE)
    time_started = models.DateTimeField(auto_now_add=True)
    time_submitted = models.DateTimeField(null=True)
    score = models.FloatField(null=True)


class QuestionCompletion(models.Model):
    quiz_attempt = models.ForeignKey(QuizAttempt, null=False, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, null=False, on_delete=models.CASCADE)
    given_answer = models.ForeignKey(AnswerChoice, null=True, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('quiz_attempt', 'question')