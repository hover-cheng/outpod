"""outpod URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from rest_framework.authtoken import views
from saltapi.views import salt_index, salt_faq, salt_login, salt_log
from saltapi.api import serverlist, grouplist, commandlist, getresult, customorder, serverinfo, updateorder, appnamelist, mvntypelist, mvnorderlist, operationlist, findserver


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^api/token-auth$', views.obtain_auth_token),

    url(r'^salt$', salt_index, name='salt_index'),
    url(r'^salt/faq$', salt_faq, name='salt_faq'),
    url(r'^salt/login$', salt_login, name="salt_login"),
    url(r'^salt/log$', salt_log, name='salt_log'),

    url(r'^api/salt/findserver$', findserver),
    url(r'^api/salt/server$', serverlist),
    url(r'^api/salt/serverinfo/(?P<id>\d+$)', serverinfo),
    url(r'^api/salt/group', grouplist),
    url(r'^api/salt/commandlist', commandlist),
    url(r'^api/salt/result', getresult),
    url(r'^api/salt/customorder', customorder),
    url(r'^api/salt/log', operationlist),
    url(r'^api/salt/updatecommand', updateorder),
    url(r'^api/salt/app', appnamelist),
    url(r'^api/salt/mvntype$', mvntypelist),
    url(r'^api/salt/mvnorder$', mvnorderlist),
]
