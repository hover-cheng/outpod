from django.shortcuts import render, redirect
import os
from saltapi.api import saltapi
import logging
logger = logging.getLogger("django")


# Create your views here.
def salt_index(request):
    content = {}
    if request.method == "GET":
        if request.COOKIES.get('token'):
            return render(request, 'salt_index.html', content)
        else:
            return redirect(to="salt_login")
    if request.method == "POST":
        f = request.FILES.get("uploadfile")
        baseDir = os.path.dirname(os.path.abspath(__name__))
        uploaddir = os.path.join(baseDir, 'collectedstatic', 'upload')
        filename = os.path.join(uploaddir, f.name)
        fobj = open(filename, 'wb')
        for chrunk in f.chunks():
            fobj.write(chrunk)
        fobj.close()
        saltapi.upload_file(f.name)
    return redirect(to="salt_index")


def salt_login(request):
    content = {}
    return render(request, "salt_login.html", content)


def salt_faq(request):
    content = {}
    return render(request, 'salt_faq.html', content)


def salt_log(request):
    content = {}
    return render(request, 'salt_log.html', content)


def salt_ssh(request):
    return render(request, 'webssh.html')


def index(request):
    return render(request, 'saltapi/index.html', {})
