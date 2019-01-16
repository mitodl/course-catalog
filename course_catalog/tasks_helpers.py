"""
course_catalog helper functions for tasks
"""
import json
import logging
import re
from datetime import datetime
import pytz
import requests
from django.db import transaction
from course_catalog.constants import PlatformType, semester_mapping, MIT_OWNER_KEYS, ocw_edx_mapping
from course_catalog.models import Course, CourseTopic, CourseInstructor, CoursePrice
from course_catalog.serializers import CourseSerializer
from course_catalog.settings import EDX_API_CLIENT_ID, EDX_API_CLIENT_SECRET


log = logging.getLogger(__name__)


def get_access_token():
    """
    Get an access token for edx
    """
    post_data = {
        "grant_type": "client_credentials",
        "client_id": EDX_API_CLIENT_ID,
        "client_secret": EDX_API_CLIENT_SECRET,
        "token_type": "jwt"
    }
    response = requests.post("https://api.edx.org/oauth2/v1/access_token", data=post_data)
    return response.json()["access_token"]


def parse_mitx_json_data(course_data):
    """
    Main function to parse edx json data
    """

    # Make sure this is an MIT course
    if not is_mit_course(course_data):
        return

    # Make changes atomically so we don't end up with partially saved/deleted data
    with transaction.atomic():

        # Get the last modified date from the course data
        course_modified = course_data.get("modified")

        # Parse each course run individually
        for course_run in course_data.get("course_runs"):
            course_run_key = course_run.get("key")

            # Get the last modified date from the course run
            course_run_modified = course_run.get("modified")

            # Since we use data from both course and course_run and they use different modified timestamps,
            # we need to find the newest changes
            max_modified = course_modified if course_modified > course_run_modified else course_run_modified

            # Try and get the course instance. If it exists check to see if it needs updating
            try:
                course_instance = Course.objects.get(course_id=course_run.get("key"))
                compare_datetime = datetime.strptime(max_modified, "%Y-%m-%dT%H:%M:%S.%fZ").astimezone(pytz.utc)
                if compare_datetime <= course_instance.last_modified:
                    # print("(" + course_data.get("key") + ", " + course_run_key + ") skipped")
                    continue
            except Course.DoesNotExist:
                course_instance = None

            year, semester = get_year_and_semester(course_run, course_run_key)

            course_fields = {
                "course_id": course_run_key,
                "title": course_run.get("title"),
                "short_description": course_run.get("short_description"),
                "full_description": course_run.get("full_description"),
                "level": course_run.get("level_type"),
                "semester": semester,
                "language": course_run.get("content_language"),
                "platform": PlatformType.mitx.value,
                "year": year,
                "start_date": course_run.get("start"),
                "end_date": course_run.get("end"),
                "enrollment_start": course_run.get("enrollment_start"),
                "enrollment_end": course_run.get("enrollment_end"),
                "image_src": (course_run.get("image") or {}).get("src"),
                "image_description": (course_run.get("image") or {}).get("description"),
                "last_modified": max_modified,
                "raw_json": json.dumps(course_data),
            }

            course_serializer = CourseSerializer(data=course_fields, instance=course_instance)
            if not course_serializer.is_valid():
                # print(course_serializer.errors)
                # print("(" + course_data.get("key") + ", " + course_run_key + ") is not valid")
                log.error("Course %s is not valid: %s", course_run_key, course_serializer.errors)
                continue
            course = course_serializer.save()
            # print("(" + course_data.get("key") + ", " + course_run_key + ") is valid")

            handle_many_to_many_fields(course, course_data, course_run)


def handle_many_to_many_fields(course, course_data, course_run):
    """
    Helper function to create or link the many to many fields
    """
    # Clear out topics and re-add them
    course.topics.clear()
    for topic in course_data.get("subjects"):
        course_topic, _ = CourseTopic.objects.get_or_create(name=topic.get("name"))
        course.topics.add(course_topic)

    # Clear out the instructors and re-add them
    course.instructors.clear()
    # In the samples it looks like instructors is never populated and staff is
    for instructor in course_run.get("staff"):
        course_instructor, _ = CourseInstructor.objects.get_or_create(first_name=instructor.get("given_name"),
                                                                      last_name=instructor.get("family_name"))
        course.instructors.add(course_instructor)

    # Clear out the prices and re-add them
    course.prices.clear()
    for price in course_run.get("seats"):
        course_price, _ = CoursePrice.objects.get_or_create(
            price=price.get("price"),
            mode=price.get("type"),
            upgrade_deadline=price.get("upgrade_deadline"),
        )
        course.prices.add(course_price)


def is_mit_course(course_data):
    """
    Helper function to determine if a course is an MIT course
    """
    for owner in course_data.get("owners"):
        if owner["key"] in MIT_OWNER_KEYS:
            return True
    return False


def get_year_and_semester(course_run, course_run_key):
    """
    Parse year and semester out of course run key.
    If course run key cannot be parsed attempt to get year from start
    """
    match = re.search("[1|2|3]T[0-9]{4}", course_run_key)
    if match:
        year = int(match.group(0)[-4:])
        semester = semester_mapping.get(match.group(0)[-6:-4])
    else:
        semester = None
        if course_run.get("start"):
            year = course_run.get("start")[:4]
        else:
            year = None

    # print(f"{course_run_key} {year} {semester}")
    return year, semester


def load_json_from_string(s):
    """
    Loads the passed string as a JSON object
    """
    return json.loads(s)


def digest_ocw_course_master_json(master_json, last_modified):
    """
    Takes in OCW course master json to store it in DB
    Returns True if the course was updated and False otherwise
    """
    with transaction.atomic():
        try:
            course_instance = Course.objects.get(course_id=master_json.get("uid"))
            # Make sure that the data we are syncing is newer than what we already have
            if last_modified <= course_instance.last_modified:
                return False
        except Course.DoesNotExist:
            course_instance = None

        course_fields = {
            "course_id": master_json.get("uid"),
            "title": master_json.get("title"),
            "short_description": master_json.get("description"),
            "level": master_json.get("course_level"),
            "semester": master_json.get("from_semester"),
            "language": master_json.get("language"),
            "platform": PlatformType.ocw.value,
            "year": master_json.get("from_year"),
            "image_src": master_json.get("image_src"),
            "image_description": master_json.get("image_description"),
            "last_modified": last_modified,
            "raw_json": master_json,
        }

        course_serializer = CourseSerializer(data=course_fields, instance=course_instance)
        if not course_serializer.is_valid():
            # course_fields.pop('raw_json')
            # print(course_fields)
            # print(course_serializer.errors)
            log.error("Course %s is not valid: %s", master_json.get("uid"), course_serializer.errors)
            return False
        course = course_serializer.save()

        # Clear previous topics, instructors, and prices
        course.topics.clear()
        course.instructors.clear()
        course.prices.clear()

        # Handle topics
        for topic_obj in master_json.get("course_collections"):
            topic_name = get_ocw_topic(topic_obj)
            if topic_name:
                course_topic, _ = CourseTopic.objects.get_or_create(name=topic_name)
                course.topics.add(course_topic)

        # Handle instructors
        for instructor in master_json.get("instructors"):
            course_instructor, _ = CourseInstructor.objects.get_or_create(first_name=instructor.get("first_name"),
                                                                          last_name=instructor.get("last_name"))
            course.instructors.add(course_instructor)

        # Handle price
        course_price, _ = CoursePrice.objects.get_or_create(price="0.00", mode="audit", upgrade_deadline=None)
        course.prices.add(course_price)
        return True


def get_ocw_topic(topic_object):
    """
    Gets ocw_feature if that fails then ocw_subfeature and if that fails then ocw_speciality
    """

    # Get topic list by specialty first, subfeature second, and feature third
    topics = (ocw_edx_mapping.get(topic_object.get("ocw_speciality")) or
              ocw_edx_mapping.get(topic_object.get("ocw_subfeature")) or
              ocw_edx_mapping.get(topic_object.get("ocw_feature")))

    return topics
