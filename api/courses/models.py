from django.db import models

class FieldOfStudy(models.Model):
    name = models.CharField(max_length=64, unique=True)


class KnowledgeLevel(models.Model):
    name = models.CharField(max_length=64, unique=True)


class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)


class CoursePrerequisite(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name="prerequisite_links")
    prerequisite = models.ForeignKey('Course', on_delete=models.CASCADE, related_name="required_for_links")

    class Meta:
        unique_together = ('course', 'prerequisite')


class Course(models.Model):
    title = models.CharField(max_length=256, null=False, unique=True)
    description = models.TextField(null=False)
    overview = models.TextField(null=False)
    knowledge_level = models.ForeignKey(KnowledgeLevel, on_delete=models.PROTECT, related_name="courses")
    fields_of_study = models.ManyToManyField(FieldOfStudy, related_name="courses")
    prerequisite_courses = models.ManyToManyField('self', through=CoursePrerequisite, symmetrical=False, related_name="required_for")
    prerequisite_knowledge = models.TextField(null=False)
    advance_preparation = models.TextField(null=False)
    is_published = models.BooleanField(default=False)
    cpe_credits = models.FloatField(null=False)
    tags = models.ManyToManyField(Tag, blank=True, related_name="courses")
    created_at = models.DateTimeField()
    reviewed_at = models.DateTimeField()


class LearningObjective(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False)
    objective = models.TextField(null=False)