from django.db import models
from django.contrib.postgres.fields import JSONField


class CourseInstructor(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)


class CourseTopic(models.Model):
    name = models.CharField(max_length=128, unique=True)


class CoursePrice(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits=5)
    mode = models.CharField(max_length=128)
    upgrade_deadline = models.DateTimeField(null=True)


class Course(models.Model):
    course_id = models.CharField(max_length=128, unique=True)
    title = models.CharField(max_length=256)
    short_description = models.CharField(max_length=1024)
    level = models.CharField(max_length=128)
    semester = models.CharField(max_length=10)
    language = models.CharField(max_length=128)
    platform = models.CharField(max_length=128)
    year = models.IntegerField()
    full_description = models.TextField(null=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    enrollment_start = models.DateTimeField(null=True)
    enrollment_end = models.DateTimeField(null=True)
    image_src = models.URLField(null=True)
    image_description = models.CharField(max_length=1024, null=True)
    raw_json = JSONField(null=True)
    instructors = models.ManyToManyField(CourseInstructor)
    topics = models.ManyToManyField(CourseTopic)
    prices = models.ManyToManyField(CoursePrice)
