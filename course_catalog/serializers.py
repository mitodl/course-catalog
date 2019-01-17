"""
course_catalog serializers
"""
from rest_framework import serializers
from .models import Course, CourseInstructor, CoursePrice, CourseTopic
from .constants import PlatformType


class CourseInstructorSerializer(serializers.ModelSerializer):
    """
    Serializer for CourseInstructor model
    """
    class Meta:
        model = CourseInstructor
        fields = "__all__"


class CoursePriceSerializer(serializers.ModelSerializer):
    """
    Serializer for CoursePrice model
    """
    class Meta:
        model = CoursePrice
        fields = "__all__"


class CourseTopicSerializer(serializers.ModelSerializer):
    """
    Serializer for CourseTopic model
    """
    class Meta:
        model = CourseTopic
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for Course model
    """
    instructors = CourseInstructorSerializer(read_only=True, many=True, allow_null=True)
    topics = CourseTopicSerializer(read_only=True, many=True, allow_null=True)
    prices = CoursePriceSerializer(read_only=True, many=True, allow_null=True)

    class Meta:
        model = Course
        # fields = "__all__"
        exclude = ('raw_json',)


class OCWCourseSerializer(serializers.ModelSerializer):
    """
    This is a serializer for de-serializing parsed OCW Plone JSON data to be saved as Course model instances
    """
    class Meta:
        model = Course
        fields = "__all__"

    def to_internal_value(self, data):
        my_fields = {
            "raw_json": data,
            # Mismatching fields
            "course_id": data.get("uid"),
            "short_description": data.get("description"),
            "level": data.get("course_level"),
            "semester": data.get("from_semester"),
            "year": data.get("from_year"),
            "start_date": data.get("creation_date"),
            "end_date": data.get("expiration_date"),
            "topics": data.get("course_collections"),
            "prices": data.get("price"),
            # Matching fields
            "title": data.get("title"),
            "language": data.get("language"),
            "image_src": data.get("image_src"),
            "image_description": data.get("image_description"),
            "instructors": data.get("instructors"),
        }
        nullable_fields = [f.name for f in Course._meta.fields if f.null]

        for field_key, field_value in my_fields.items():
            # Raise validation error if value is empty but is not nullable
            if not field_value and field_key not in nullable_fields:
                raise serializers.ValidationError({
                    field_key: "This field is required."
                })

        return {key: val for key, val in my_fields.items()}

    def create(self, validated_data):
        instructors = validated_data.pop("instructors")
        topics = validated_data.pop("topics")
        prices = validated_data.pop("prices")

        course = Course.objects.create(platform=PlatformType.ocw, **validated_data)

        # Create and attach instructors
        for i in instructors:
            CourseInstructor.objects.create(course=course, first_name=i.get("first_name"),
                                            last_name=i.get("last_name"))
        # Create and attach topics
        for t in topics:
            CourseTopic.objects.create(course=course, name=t.get("ocw_feature"))
        # Create and attach prices
        CoursePrice.objects.create(course=course, **prices)

        return course
