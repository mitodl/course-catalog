
import requests
from celery.task import task

from course_catalog.tasks_helpers import get_access_token, parse_mitx_json_data


@task
def get_edx_data():
    url = "https://api.edx.org/catalog/v1/catalogs/248/courses"
    while True:
        # print(url)
        access_token = get_access_token()
        response = requests.get(url, headers={"Authorization": "JWT " + access_token})
        for course_data in response.json()["results"]:
            parse_mitx_json_data(course_data)

        # print(response.json()["next"])
        if response.json()["next"]:
            url = response.json()["next"]
        else:
            break
