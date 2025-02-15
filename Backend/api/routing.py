from django.urls import re_path
from api.consumers import EmployeeConsumer,ProjectConsumer

websocket_urlpatterns = [
    re_path(r'ws/employees/$', EmployeeConsumer.as_asgi()),
    re_path(r'ws/projects/$', ProjectConsumer.as_asgi()),
]
