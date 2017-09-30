一个基于salt-api的服务器管理系统

需要在salt-master上部署salt-api服务

在业务的saltapi.py里面编写向salt-master发送的api的指令格式
在业务的api.py里面编写业务的api接口，通过post方法将前端数据传到后端，并且调用saltapi.py中各种api指令的方法

功能
1.可以自定义一些常用的salt指令
2.可以手动输入salt指令
3.可以对指定的项目打包，下发文件
