"""
course_catalog models
"""
from django.db import models
from django.contrib.postgres.fields import JSONField


class TimestampedModel(models.Model):
    """
    Parent class for all models under course_catalog app.
    It provides created_on and last_updated timestamps automatically.
    """
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CourseInstructor(TimestampedModel):
    """
    Instructors for all courses
    """
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)


class CourseTopic(TimestampedModel):
    """
    Topics for all courses (e.g. "History")
    """
    name = models.CharField(max_length=128, unique=True)


class CoursePrice(TimestampedModel):
    """
    Price model for all courses (e.g. "price": 0.00, "mode": "audit")
    """
    price = models.DecimalField(decimal_places=2, max_digits=5)
    mode = models.CharField(max_length=128)
    upgrade_deadline = models.DateTimeField(null=True)


class Course(TimestampedModel):
    """
    Course model for courses on all platforms
    """
    course_id = models.CharField(max_length=128, unique=True)
    title = models.CharField(max_length=256)
    short_description = models.CharField(max_length=1024, null=True)
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
    last_modified = models.DateTimeField(null=True)
    raw_json = JSONField(null=True)
    instructors = models.ManyToManyField(CourseInstructor, blank=True, related_name="courses")
    topics = models.ManyToManyField(CourseTopic, blank=True, related_name="courses")
    prices = models.ManyToManyField(CoursePrice, blank=True, related_name="courses")
