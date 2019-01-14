"""
course_catalog tasks
"""
import logging

import requests
import boto3
from celery.task import task
from course_catalog.settings import EDX_API_URL
from django.conf import settings
from ocw_data_parser import OCWParser
from course_catalog.tasks_helpers import (get_access_token,
                                          parse_mitx_json_data,
                                          load_json_from_string,
                                          digest_master_json)
from course_catalog.constants import NON_COURSE_DIRECTORIES


log = logging.getLogger(__name__)


@task
def get_edx_data():
    """
    Task to sync mitx data with the database
    """
    url = EDX_API_URL
    while url:
        # print(url)
        access_token = get_access_token()
        response = requests.get(url, headers={"Authorization": "JWT " + access_token})
        if response.status_code == 200:
            for course_data in response.json()["results"]:
                try:
                    parse_mitx_json_data(course_data)
                except Exception:  # pylint: disable=broad-except
                    log.exception("Error encountered parsing MITx json")
        else:
            log.error("Bad response status %s for %s", str(response.status_code), url)
            break

        url = response.json()["next"]


@task
def get_ocw_data():
    """
    Task to sync OCW course data with database
    """
    upload_bucket = {
        "name": settings.OCW_LEARNING_COURSE_BUCKET_NAME,
        "access_key": settings.OCW_LEARNING_COURSE_ACCESS_KEY,
        "secret_key": settings.OCW_LEARNING_COURSE_SECRET_KEY
    }

    raw_data_bucket = boto3.resource('s3',
                                     aws_access_key_id=settings.OCW_CONTENT_ACCESS_KEY,
                                     aws_secret_access_key=settings.OCW_CONTENT_SECRET_KEY
                                     ).Bucket(name=settings.OCW_CONTENT_BUCKET_NAME)
    # Get all the courses keys
    ocw_courses = set()
    for file in raw_data_bucket.objects.all():
        key_pieces = file.key.split("/")
        course_prefix = key_pieces[0] + "/" + key_pieces[1]
        if course_prefix not in NON_COURSE_DIRECTORIES:
            ocw_courses.add("/".join(key_pieces[:-2]))

    # Query S3 Bucket for JSONs per course
    loaded_raw_jsons_for_course = []
    for course_prefix in ocw_courses:
        for obj in raw_data_bucket.objects.filter(Prefix=course_prefix):
            loaded_raw_jsons_for_course.append(load_json_from_string(obj.get()["Body"].read()))
    parser = OCWParser(list_of_loaded_jsons=loaded_raw_jsons_for_course)
    parser.setup_s3_uploading(upload_bucket)
    parser.upload_all_media_to_s3()
    master_json = parser.get_master_json()
    digest_master_json(master_json)
