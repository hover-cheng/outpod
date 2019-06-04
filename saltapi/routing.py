from django.conf.urls import url
from saltapi import consumers

websocket_urlpatterns = [
    url(r'^ssh/', consumers.SSHClient),
]
