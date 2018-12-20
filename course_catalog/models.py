from django.db import models
from django.contrib.postgres.fields import JSONField


class Course(models.Model):
    title = models.CharField(max_length=256)
    short_description = models.CharField(max_length=1024)
    level = models.CharField(max_length=128)
    semester = models.CharField(max_length=10)
    language = models.CharField(max_length=128)
    platform = models.CharField(max_length=128)
    year = models.IntegerField()
    id = models.CharField(max_length=128, unique=True)
    full_description = models.TextField(null=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    enrollment_start = models.DateTimeField(null=True)
    enrollment_end = models.DateTimeField(null=True)
    image = JSONField(null=True)
    topics = JSONField()
    prices = JSONField()
    instructors = JSONField()
    mode_types = JSONField()
    raw_json = JSONField(null=True)
