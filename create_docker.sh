#!/bin/bash
DATE=`date +'%Y%m%d%H%M'`
homebase=/home/opt/svnbase
#svnurl=$1
appname=$1
projectpath=/home/opt/docker/$1

if [ ! -d $projectpath ];then
    echo "create new docker: appname"
    cp -rf /home/opt/docker/docker_jdk_template $projectpath
    sed -i "s#ADD ./project.jar /home/opt/project/#ADD ./$appname.jar /home/opt/project/#g" $projectpath/Dockerfile
    sed -i "s#/home/opt/project/project.jar#/home/opt/project/$appname.jar#g" $projectpath/run.sh
fi

mv /tmp/$appname.jar /home/opt/docker/$appname/$appname.jar

cd /home/opt/docker/$appname/ && docker build -t $appname/jdk_$DATE .
docker stop $appname
docker rm $appname
docker run -d -v /home/logs/:/logs/ --name $appname $appname/jdk_$DATE /home/opt/scripts/run.sh

