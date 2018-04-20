#!/bin/bash

#config the java home
JAVA_HOME="/home/opt/tools/jdk"
CLASS_PATH="$JAVA_HOME/lib:$JAVA_HOME/jre/lib"
PATH=".:$PATH:$JAVA_HOME/bin"
export JAVA_HOME

DATE=`date +'%Y%m%d%H%M'`
NUM=`ps aux |grep java |grep -v grep |wc -l`
YN=project.war
PROJECTNAME=project
BASEPATH=/home/opt/tools/tomcat/webapps/
HOMEPATH=/home/opt/tools/tomcat/
BAKPATH=/home/opt/databackup/

#backup the project
if [ ! -d $BAKPATH ];then
mkdir -p $BAKPATH
fi

if [ -f $BASEPATH/$YN ];then
	cp -f $BASEPATH/$YN $BAKPATH/$YN.bak$DATE
fi
if [ -d $BASEPATH/$PROJECTNAME ];then
	cp -rf $BASEPATH/$PROJECTNAME $BAKPATH/$PROJECTNAME.bak$DATE
fi

#更新war包,将包含war包的压缩文件解压到/tmp目录下，然后运行./update_tomcate.sh war进行更新操作
function update_war ()
{
    cd /tmp && tar zxvf $PROJECTNAME.tar.gz
	if [ $NUM != 0 ];then
	$HOMEPATH/bin/shutdown.sh
	sleep 5
	PID=`ps aux |grep java |grep -v grep |awk '{print $2}'`
	NUM_new=`ps aux |grep java |grep -v grep |wc -l`
  		if [ $NUM_new == 0 ];then
      			echo -e "mjava is shutdown..."
      			rm -f $BASEPATH/$YN
      			rm -rf $BASEPATH/$PROJECTNAME
      			cp /tmp/$YN $BASEPATH/
      			$HOMEPATH/bin/startup.sh
     			sleep 5
  		else
      		echo -e "java is not shutdown,java will kill by -9"
      		kill -9 $PID
      			rm -f $BASEPATH/$YN
      			rm -rf $BASEPATH/$PROJECTNAME
      			cp /tmp/$YN $BASEPATH/
      			$HOMEPATH/bin/startup.sh
  		fi
	echo -e "update is complate..."
    rm -rf /tmp/$YN
    rm -rf /tmp/$PROJECTNAME
    rm -rf /tmp/$PROJECTNAME.tar.gz
	else 
		echo -e "java is not runing,please check....."
	fi
}
#更新补丁包，将包含更新的压缩文件解压到/tmp目录下，然后运行./update_tomcate.sh patch进行更新操作
function update_patch ()
{
    cd /tmp && tar zxvf $PROJECTNAME.tar.gz
	if [ $NUM != 0 ];then
	$HOMEPATH/bin/shutdown.sh
	sleep 5
	PID=`ps aux |grep java |grep -v grep |awk '{print $2}'`
	NUM_new=`ps aux |grep java |grep -v grep |wc -l`
  		if [ $NUM_new == 0 ];then
      			echo -e "mjava is shutdown..."
      			cp -rf /tmp/$PROJECTNAME $BASEPATH/
      			$HOMEPATH/bin/startup.sh
     			sleep 5
  		else
      		echo -e "mjava is not shutdown,java will kill by -9"
      		kill -9 $PID
      			cp -rf /tmp/$PROJECTNAME $BASEPATH/
      			$HOMEPATH/bin/startup.sh
  		fi
	echo -e "mupdate is complate..."
    rm -rf /tmp/$YN
    rm -rf /tmp/$PROJECTNAME
    rm -rf /tmp/$PROJECTNAME.tar.gz
	else 
		echo -e "mjava is not runing,please check....."
	fi
}
#read -p "Please input your choice(war|patch):" num

function start_tomcat()
{
    PID=`ps aux |grep java |grep -v grep |awk '{print $2}'`
    NUM_new=`ps aux |grep java |grep -v grep |wc -l`
    if [ $NUM_new == 0 ];then
        $HOMEPATH/bin/startup.sh
    fi
}

function stop_tomcat()
{
    NUM=`ps aux |grep java |grep -v grep |wc -l`
    if [ $NUM != 0 ];then
        $HOMEPATH/bin/shutdown.sh
        sleep 10
        PID=`ps aux |grep java |grep -v grep |awk '{print $2}'`
        NUM_new=`ps aux |grep java |grep -v grep |wc -l`
        if [ $NUM_new != 0 ];then
            kill -9 $PID
        fi
    fi

}

case $1 in
	"war")
		update_war
	;;
	"patch")
		update_patch
	;;
	"start")
		start_tomcat
	;;
	"stop")
		stop_tomcat
	;;
	*)
		echo "Usage: $0 {war|patch|start|stop}"
		exit 1
	;;
esac

