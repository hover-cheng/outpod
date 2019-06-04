from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
import paramiko
import json
import time
import sys
from saltapi.sshclient import SSH


# 使用WebSocket实现Webssh功能
class SSHClient(WebsocketConsumer):
    message = {'message': None}
    # message = None

    def connect(self):
        hostip = self.scope['query_string'].strip()
        self.accept()
        self.ssh = SSH(websocker=self, message=self.message)
        self.ssh.connect(host=hostip)

    def receive(self, text_data):
        self.ssh.shell(text_data)

    def disconnect(self, close_code):
        self.ssh.django_to_ssh('exit\n')
        self.close()
