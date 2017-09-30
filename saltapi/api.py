from rest_framework import serializers, status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from saltapi.models import GroupList, ServerList, CommandList, OperationLog, ProjectList, AppName, MvnType, MvnOrder, UserProfile
from saltapi import saltapi
from django.contrib.auth.models import User

import logging
logger = logging.getLogger("scripts")


class GroupInfo(serializers.ModelSerializer):
    class Meta:
        model = GroupList
        fields = '__all__'
        depth = 1


class ServerInfo(serializers.ModelSerializer):
    class Meta:
        model = ServerList
        fields = '__all__'
        depth = 2


class CommandInfo(serializers.ModelSerializer):
    class Meta:
        model = CommandList
        fields = '__all__'


class OperationInfo(serializers.ModelSerializer):
    class Meta:
        model = OperationLog
        fields = '__all__'


class AppInfo(serializers.ModelSerializer):
    class Meta:
        model = AppName
        fields = '__all__'


class MvntyepInfo(serializers.ModelSerializer):
    class Meta:
        model = MvnType
        fields = '__all__'


class MvnorderInfo(serializers.ModelSerializer):
    class Meta:
        model = MvnOrder
        fields = '__all__'


@api_view(["GET"])
@authentication_classes((TokenAuthentication,))
def appnamelist(request):
    if request.method == 'GET' and request.COOKIES.get("token"):
        appnamelist = AppName.objects.all()
        ser = AppInfo(appnamelist, many=True)
        return Response(ser.data)


@api_view(["GET"])
@authentication_classes((TokenAuthentication,))
def mvntypelist(request):
    if request.method == 'GET' and request.COOKIES.get("token"):
        mvntype = MvnType.objects.all()
        ser = MvntyepInfo(mvntype, many=True)
        return Response(ser.data)


@api_view(["GET"])
@authentication_classes((TokenAuthentication,))
def mvnorderlist(request):
    if request.method == "GET" and request.COOKIES.get("token"):
        mvnorder = MvnOrder.objects.all()
        ser = MvnorderInfo(mvnorder, many=True)
        return Response(ser.data)


@api_view(["GET"])
@authentication_classes((TokenAuthentication,))
def operationlist(request):
    if request.method == "GET" and request.user.username == "admin":
        operationlist = OperationLog.objects.order_by('-id')
        ser = OperationInfo(operationlist, many=True)
        return Response(ser.data)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(["GET"])
@authentication_classes((TokenAuthentication,))
def commandlist(request):
    if request.method == "GET" and request.COOKIES.get("token"):
        commandlist = CommandList.objects.all()
        ser = CommandInfo(commandlist, many=True)
        return Response(ser.data)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(["GET"])
@authentication_classes((TokenAuthentication,))
def serverlist(request):
    if request.method == "GET" and request.COOKIES.get("token"):
        serverlist = ServerList.objects.all()
        ser = ServerInfo(serverlist, many=True)
        return Response(ser.data)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(["GET"])
@authentication_classes((TokenAuthentication,))
def serverinfo(request, id):
    if request.method == "GET" and request.COOKIES.get("token"):
        id = id
        groupinfo = GroupList.objects.get(id=id)
        serverinfo = ServerList.objects.filter(belong_to=groupinfo).order_by('ip')
        ser = ServerInfo(serverinfo, many=True)
        return Response(ser.data)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(["POST"])
@authentication_classes((TokenAuthentication,))
def findserver(request):
    if request.method == "POST" and request.COOKIES.get("token"):
        id = request.POST['groupid'].split(',')
        ip = request.POST['ip']
        groups = GroupList.objects.filter(id__in=id)
        serverinfo = ServerList.objects.filter(belong_to__in=groups, ip__contains=ip).order_by('ip')
        if not serverinfo:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            ser = ServerInfo(serverinfo, many=True)
            return Response(ser.data)


@api_view(["GET"])
@authentication_classes((TokenAuthentication,))
def grouplist(request):
    if request.method == "GET" and request.COOKIES.get("token"):
        user = User.objects.get(username=request.user.username)
        userper = UserProfile.objects.get(belong_to=user)
        permission = userper.userpermission
        permission = permission.strip().split(',')
        if permission == ['ALL']:
            serverlist = GroupList.objects.all().order_by('name')
            ser = GroupInfo(serverlist, many=True)
            return Response(ser.data)
        elif permission != ['']:
            pro = ProjectList.objects.filter(name__in=permission)
            serverlist = GroupList.objects.filter(belong_to__in=pro).order_by('name')
            ser = GroupInfo(serverlist, many=True)
            return Response(ser.data)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
def getresult(request):
    if request.method == "POST" and request.COOKIES.get("token"):
        username = request.user.first_name
        check_box_list = request.POST.getlist("serverlist")
        commandid = request.POST["command"]
        command = CommandList.objects.get(id=commandid)
        serverlist = ','.join(check_box_list)
        resultinfo = saltapi.send_command(serverlist, command.command)
        iplist = serverlist.split(',')
        for ip in iplist:
            createlog = OperationLog.objects.create(
                ip=ip,
                operation=command.command,
                operator=username,
            )
        result = []
        for info in resultinfo:
            tmp = {"ip": info, "result": resultinfo[info]}
            result.append(tmp)
        return Response(result)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
def customorder(request):
    if request.method == "POST" and request.COOKIES.get("token"):
        username = request.user.first_name
        check_box_list = request.POST.getlist("serverlist")
        command = request.POST["command"]
        arg1 = request.POST['arg1']
        arg2 = request.POST['arg2']
        code = request.POST['code']
        tmparg = arg1 + " " + arg2
        if code == "iamgod" and "rm" not in tmparg.split() and request.user.username != "admin":
            serverlist = ','.join(check_box_list)
            resultinfo = saltapi.custom_command(serverlist, command, arg1, arg2)
            iplist = serverlist.split(',')
            for ip in iplist:
                createlog = OperationLog.objects.create(
                    ip=ip,
                    operation=command + " " + arg1 + " " + arg2,
                    operator=username,
                )
            result = []
            for info in resultinfo:
                tmp = {"ip": info, "result": resultinfo[info]}
                result.append(tmp)
            return Response(result)
        elif code == "iamgod" and request.user.username == "admin":
            serverlist = ','.join(check_box_list)
            resultinfo = saltapi.custom_command(serverlist, command, arg1, arg2)
            iplist = serverlist.split(',')
            for ip in iplist:
                createlog = OperationLog.objects.create(
                    ip=ip,
                    operation=command + " " + arg1 + " " + arg2,
                    operator=username,
                )
            result = []
            for info in resultinfo:
                tmp = {"ip": info, "result": resultinfo[info]}
                result.append(tmp)
            return Response(result)
        elif code != "iamgod":
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        elif "rm" in tmparg.split():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
def updateorder(request):
    if request.method == "POST" and request.COOKIES.get("token"):
        code = request.POST['code']
        if code == "iamgod":
            username = request.user.first_name
            check_box_list = request.POST.getlist("serverlist")
            appname = request.POST["appname"]
            svnurl = request.POST['svnurl']
            buildcommand = request.POST['buildcommand']
            buildtype = request.POST['buildtype']
            arg1 = 'salt://upload/' + appname + '.' + buildtype
            arg2 = '/tmp/' + appname + '.' + buildtype
            serverlist = ','.join(check_box_list)
            if buildtype == 'war':
                updatecommand = '/home/opt/scripts/update_tomcat.sh war'
            elif buildtype == 'jar':
                updatecommand = '/home/opt/scripts/create_docker.sh %s' % appname
            result = []
            resultinfo = saltapi.update_command(appname, buildtype, buildcommand, svnurl)
            for info in resultinfo:
                tmp = {"ip": info, "result": resultinfo[info]}
                result.append(tmp)
            if 'success' in resultinfo[info]:
                resultinfo = saltapi.rsync_file(serverlist, arg1, arg2)
                for info in resultinfo:
                    tmp = {"ip": info, "result": resultinfo[info]}
                    result.append(tmp)
                resultinfo = saltapi.send_command(serverlist, updatecommand)
                iplist = serverlist.split(',')
                for ip in iplist:
                    createlog = OperationLog.objects.create(
                        ip=ip,
                        operation='Version update: ' + appname + "." + buildtype,
                        operator=username,
                    )
                for info in resultinfo:
                    tmp = {"ip": info, "result": resultinfo[info]}
                    result.append(tmp)
            return Response(result)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
