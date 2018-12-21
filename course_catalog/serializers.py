from rest_framework import serializers
from .models import Course


class CourseSerializer(serialiIzers.ModelSerializer):
    class Meta:
        model = Course
        fields = ""
    
    def create(self, validated_data):
        platform = self.initial_data.get("platform")
        course_fields = ["course_id", "title", "short_description", "full_description", "level", "semester", "language",
                         "platform", "year", "start_date", "end_date", "enrollment_start", "enrollment_end", "image",
                         "raw_json"]
        fields_to_serialize = []
        data = {x: None for x in course_fields}
        if platform == "OCW":
            fields_to_serialize = {
                "course_id": "uid",
                "title": "title",
                "short_description": "description",
                "level": "course_level",
                "semester": "from_semester",
                "year": "from_year",
                "language": "language"
            }
            # image: Need to be generated from master json's initial data
            #  full_description = None, start_date= = None, end_date = None, enrollment_start = None,
            #  enrollment_end = None
            # raw_json: TBD
            for key in course_fields:
                if key in fields_to_serialize:
                    data[key] = self.initial_data.get(fields_to_serialize.get(key))
            data["platform"] = "OCW"
            
        elif platform == "EDX":
            fields_to_serialize = ["uuid", "title", "short_description", "full_description", "level_type",
                                   "course_runs.start", "course_runs.end", "course_runs.enrollment_start",
                                   "course_runs.enrollment_end", "image", "language"]
        
        course = Course.objects.create(**data)
        
        return course
