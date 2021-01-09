from django.urls import path, include
from .views import GetAllLogs

urlpatterns = [
    path('', GetAllLogs.as_view(), name='get_all_logs'),
]
