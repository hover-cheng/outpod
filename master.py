# -*- coding: utf-8 -*-
'''
This runner is used only for test purposes and servers no production purpose
'''
from __future__ import absolute_import
from __future__ import print_function
# Import python libs
import salt.config
import re
import os
import sys
import time


def view_directory(filename=""):
    result = os.popen('ls /home/%s' % filename).readlines()
    return result


def group(path='/etc/salt/master'):
    opts = salt.config.client_config(path)
    return opts["nodegroups"]


def get_group(path='/etc/salt/master.d/group.conf'):
    f = open(path)
    group = f.readlines()
    f.close()
    return group[1:]


def update_group(gruop, newip, path='/etc/salt/master.d/group.conf'):
    bakpath = path + '.bak'
    f = open(path)
    substance = f.readlines()
    f.close()
    if os.path.isfile(bakpath):
        os.remove(bakpath)
    os.rename(path, bakpath)
    for i in substance:
        if i.find(gruop + ":") >= 0:
            oldgruop = i
            c = i.split("'")
            c.insert(len(c) - 1, newip)
            d = ",".join(c[1:-1])
            newgroup = "'".join([c[0], d, c[-1]])
            substance[substance.index(oldgruop)] = newgroup
            f = open(path, "w")
            f.writelines(substance)
            f.close()


def buildproject(project, buildtype, buildcommand, svnurl):
    username = 'admin'
    password = '123456'
    svnbase = '/home/data/svnbase/'
    saltbase = '/home/data/salt/upload'

    projecturl = svnurl
    project = project
    buildtype = buildtype
    buildcommand = buildcommand
    projectfile = svnbase + project
    if not os.path.exists(projectfile):
        os.mkdir(projectfile)
    svnresult = os.system('cd %s && svn co  --username %s --password %s %s' % (projectfile, username, password, projecturl))
    result = {}
    if svnresult == 0:
        projectpath = svnbase + project + '/' + svnurl.split('/')[-1]
        mvnresult = os.system('cd %s  && %s' % (projectpath, buildcommand))
        if buildtype == 'war':
            mvto = os.system('mv %s/target/%s.war %s/%s.war' % (projectpath, project, saltbase, project))
        elif buildtype == 'jar':
            mvto = os.system('mv %s/target/%s.jar %s/%s.jar' % (projectpath, project, saltbase, project))
        if mvto == 0:
            result['master'] = 'project building successful'
        else:
            result['master'] = 'project building failed'
        return result
    else:
        result['master'] = 'svn checkout failed'
        return result
