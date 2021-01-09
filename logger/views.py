from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from users.permissions import IsSuperAdminUser
from .models import MongoLogsClient


class GetAllLogs(APIView):
    """Returns all logs
    """

    permission_classes = (IsSuperAdminUser,)

    def get(self, request, *args, **kwargs):

        log_type = request.GET.get('type', None)
        try:
            logs = MongoLogsClient().get_logs(log_type)
        except:
            raise ValidationError("Invalid log type")

        return Response(logs, status=200)
