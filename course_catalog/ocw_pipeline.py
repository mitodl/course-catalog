from ocw_data_parser import OCWParser
from .serializers import CourseSerializer
import json


def serialize_ocw_courses(path_to_course_root_dir):
    obj = OCWParser("/Users/method/Desktop/s3_bucket_downloader/content/PROD/22/22.THT/Fall_2015/22-tht-undergraduate-thesis-tutorial-fall-2015/",
                    "/Users/method/Desktop/geez/")
    master_json = obj.get_master_json()
    master_json["platform"] = "OCW"
    ser = CourseSerializer(data=master_json)
    if ser.is_valid():
        ser.save()
        print("Saved in DB!")
    else:
        print(ser.errors)
    return ser
