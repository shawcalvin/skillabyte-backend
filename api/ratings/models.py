from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from api.users.models import Learner
from api.courses.models import Course

class RatingCategory(models.Model):
    title = models.CharField(max_length=255)
    prompt = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)


class CourseRating(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='ratings')
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE)
    comments = models.TextField(null=True)
    date_submitted = models.DateTimeField(auto_now_add=True)


class CourseRatingEntry(models.Model):
    category = models.ForeignKey(RatingCategory, on_delete=models.PROTECT)
    rating = models.ForeignKey(CourseRating, on_delete=models.CASCADE, related_name='entries')
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])