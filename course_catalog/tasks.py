"""
course_catalog tasks
"""
import requests
from celery.task import task

from course_catalog.tasks_helpers import get_access_token, parse_mitx_json_data


@task
def get_edx_data():
    """
    Task to sync mitx data with the database
    """
    url = "https://api.edx.org/catalog/v1/catalogs/248/courses"
    while url:
        # print(url)
        access_token = get_access_token()
        response = requests.get(url, headers={"Authorization": "JWT " + access_token})
        for course_data in response.json()["results"]:
            parse_mitx_json_data(course_data)

        url = response.json()["next"]
