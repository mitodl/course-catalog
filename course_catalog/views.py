"""
course_catalog views
"""
import json

from django.conf import settings
from django.shortcuts import render
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from course_catalog.models import Course
from course_catalog.serializers import CourseSerializer
from course_catalog.templatetags.render_bundle import public_path


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


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset for Courses
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(methods=['GET'], detail=False)
    def new(self, request):
        """
        Get new courses
        """
        serializer = self.serializer_class(self.queryset.order_by('-created_on')[:10], many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False)
    def upcoming(self, request):
        """
        Get upcoming courses
        """
        serializer = self.serializer_class(
            self.queryset.filter(start_date__gt=timezone.now()).order_by('start_date')[:10],
            many=True
        )
        return Response(serializer.data)

    @action(methods=['GET'], detail=False)
    def featured(self, request):
        """
        Get featured courses
        """
        serializer = self.serializer_class(self.queryset.filter(featured=True)[:10], many=True)
        return Response(serializer.data)
