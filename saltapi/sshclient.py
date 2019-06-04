import paramiko
from threading import Thread
import socket
import json
import time
import multiprocessing


class SSH:
    def __init__(self, websocker, message):
        self.websocker = websocker
        self.message = message

    def connect(self, host, user='root', password='shmilu', pkey=None, port=22, timeout=30,
                term='xterm', pty_width=80, pty_height=24):
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(username=user, password=password, hostname=host, port=port, timeout=timeout)

            transport = ssh_client.get_transport()
            self.channel = transport.open_session()
            self.channel.get_pty(term=term, width=pty_width, height=pty_height)
            self.channel.invoke_shell()
            time.sleep(2)
            recv = self.channel.recv(1024).decode()
            # recv = recv.split('\n')
            # recv = ('\r\n' + '\n'.join(recv[1:]))
            # self.message['status'] = 0
            self.message['message'] = recv
            # message = json.dumps(self.message)
            # self.message = {'message': recv}
            message = json.dumps(self.message)
            self.websocker.send(message)

        except socket.timeout as e:
            # self.message['status'] = 1
            self.message['message'] = 'ssh 连接超时'
            message = json.dumps(self.message)
            self.websocker.send(message)
            self.websocker.close()
        except Exception as e:
            # self.message['status'] = 1
            self.message['message'] = str(e)
            message = json.dumps(self.message)
            self.websocker.send(message)
            self.websocker.close()

    def resize_pty(self, cols, rows):
        self.channel.resize_pty(width=cols, height=rows)

    def django_to_ssh(self, data):
        try:
            self.channel.send(data)
            return
        except:
            self.channel.send('exit\n')
            self.close()

    def websocket_to_django(self, data):
        try:
            while True:
                recv = self.channel.recv(65535).decode()
                # print(i, 'recv:' + recv.strip(), 'data:' + data.strip())
                # recv = ('\r\n' + '\n'.join(recv[1:]))
                if not recv:
                    return
                # self.message['status'] = 0
                self.message['message'] = recv
                # self.message = {'message': recv}
                message = json.dumps(self.message)
                self.websocker.send(message)
        except:
            self.channel.send('exit\n')
            self.close()

    def close(self):
        self.channel.send('exit\n')
        # self.message['status'] = 1
        self.message['message'] = '关闭连接'
        # self.message = {"message": "关闭连接"}
        message = json.dumps(self.message)
        self.websocker.send(message)
        self.channel.close()
        self.websocker.close()

    def shell(self, data):
        Thread(target=self.django_to_ssh, args=(data,)).start()
        Thread(target=self.websocket_to_django, args=(data,)).start()
