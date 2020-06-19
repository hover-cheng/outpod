### 一个基于salt-api的服务器管理系统

需要在salt-master上部署salt-api服务

在业务的saltapi.py里面编写向salt-master发送的api的指令格式
在业务的api.py里面编写业务的api接口，通过post方法将前端数据传到后端，并且调用saltapi.py中各种api指令的方法
；使用mysql存储数据，需要在setting.py配置数据库的信息

* 主要功能
>* 自定义一些常用的salt指令
>* 手动输入salt指令
>* 对指定的项目打包，下发文件

使用方法:\
1.在salt-master服务器上部署salt-api，并且配置运行用户名密码\
2.将master.py上传到salt-master服务器的site-packages/salt/runners/目录下\
3.将项目代码部署到服务器，并配置代码saltapi.py中的salturl、user、password\
4.初始化项目数据库\
5.启动项目\
6.在admin管理配置服务器的，ProjectList（服务所属项目，用于权限管理），GroupList(服务器所属的业务组），AppName(服务器上的业务名称，用于自动更新），ServerList（服务器信息)，CommandList（自定义执行指令），MvnOrder（manven打包指令)，MvnType(打包类型，用户判断更新调用的脚本)，OperationLog(操作日志)\
7.将项目中的update_tomcat.sh和create_docker.sh上传到minion服务器的/home/opt/scripts/目录下，用户调用更新脚本


#### 新增使用admin用户登陆可调用webssh远程登陆功能


### Requirements
Python 3.6.2\
Django 1.11.7\
djangorestframework 3.7.3\
channels 2.1.6\
mysqlclient 1.3.12
