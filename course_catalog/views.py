"""
course_catalog views
"""
import json

from django.conf import settings
from django.shortcuts import render
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from course_catalog.models import Course
from course_catalog.serializers import CourseSerializer
from course_catalog.templatetags.render_bundle import public_path
from course_catalog.constants import PlatformType
# pylint:disable=unused-argument


def index(request):
    """
    The index view. Display available programs
    """

    js_settings = {
        "gaTrackingID": settings.GA_TRACKING_ID,
        "public_path": public_path(request),
    }

    return render(request, "index.html", context={
        "js_settings_json": json.dumps(js_settings),
    })


@api_view(['GET'])
def ocw_course_report(request):
    """
    Returns a JSON object reporting OCW course sync statistics
    """
    ocw_courses = Course.objects.filter(platform=PlatformType.ocw.value, is_resource=False)
    published_ocw_courses_with_image = ocw_courses.filter(published=True, image_src__isnull=False).count()
    unpublished_ocw_courses = ocw_courses.filter(published=False).count()
    ocw_courses_without_image = ocw_courses.filter(image_src="").count()
    ocw_resources = Course.objects.filter(platform=PlatformType.ocw.value, is_resource=True).count()
    return Response({"total_number_of_ocw_courses": ocw_courses.count(),
                     "published_ocw_courses_with_image": published_ocw_courses_with_image,
                     "unpublished_ocw_courses": unpublished_ocw_courses,
                     "ocw_courses_without_image": ocw_courses_without_image,
                     "ocw_resources": ocw_resources})


class CoursePagination(LimitOffsetPagination):
    """
    Pagination class for CourseViewSet which gets default_limit and max_limit from settings
    """
    default_limit = settings.COURSE_API_DEFAULT_LIMIT
    max_limit = settings.COURSE_API_MAX_LIMIT


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset for Courses
    """

    queryset = Course.objects.all().prefetch_related('topics', 'instructors', 'prices')
    serializer_class = CourseSerializer
    pagination_class = CoursePagination

    @action(methods=['GET'], detail=False)
    def new(self, request):
        """
        Get new courses
        """
        page = self.paginate_queryset(self.queryset.order_by('-created_on'))
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(methods=['GET'], detail=False)
    def upcoming(self, request):
        """
        Get upcoming courses
        """
        page = self.paginate_queryset(self.queryset.filter(start_date__gt=timezone.now()).order_by('start_date'))
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(methods=['GET'], detail=False)
    def featured(self, request):
        """
        Get featured courses
        """
        page = self.paginate_queryset(self.queryset.filter(featured=True))
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
