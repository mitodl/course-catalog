from django.db import models
from django.contrib.postgres.fields import JSONField


class Course(models.Model):
    id = models.CharField(max_length=128, unique=True)
    title = models.CharField(max_length=256)
    short_description = models.CharField(max_length=1024, null=True)
    full_description = models.TextField()
    level = models.CharField(max_length=128)
    topics = JSONField()
    start_date = models.CharField(max_length=128)
    end_date = models.CharField(max_length=128)
    enrollment_start = models.CharField(max_length=128)
    enrollment_end = models.CharField(max_length=128)
    semester = models.CharField(max_length=128)
    year = models.CharField(max_length=128)
    instructors = JSONField()
    image = JSONField()
    video = JSONField()
    min_effort = models.IntegerField()
    max_effort = models.IntegerField()
    prerequisites = models.CharField(max_length=1024)
    mode_types = JSONField()
    prices = JSONField()
    currency = models.CharField(max_length=128)
    program = models.CharField(max_length=128)
    language = models.CharField(max_length=128)
    platform = models.CharField(max_length=128)
