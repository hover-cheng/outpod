var vm = new Vue({
  el:"#app",
  data:{
    groupinfo:[],
    server:[],
    command:[],
    selected:0,
    checkedValue:[],
    radioValue:0,
    result:[],
    customorder:"",
    arg1:"",
    arg2:"",
    code:"",
    svnurl:"",
    showloading:0,
    showORnot:0,
    selectall:"",
    username:Cookies.get("username"),
    appValue:0,
    mvnValue:0,
    typeValue:0,
    butstatus:"",
    appname:[],
    mvntype:[],
    mvnorder:[],
    serverip:"",
  },
  methods:{
    getgroup:function () {
      var self = this;
      reqwest({
        url:"api/salt/group",
        type:"json",
        headers:Cookies.get('token')? {'Authorization': 'token ' + Cookies.get('token')}:{},
        method:"get",
        success:function(res){
          self.groupinfo = res;
        },
        error:function(data){
          if (data.status == 403) {
            alert("请求被拒绝,请登陆系统");
            window.location.href="/salt/login";
          }
        },
      });
    },
    getappname:function () {
      var self = this;
      reqwest({
        url:"api/salt/appname",
        type:"json",
        headers:Cookies.get('token')? {'Authorization': 'token ' + Cookies.get('token')}:{},
        method:"get",
        success:function(res){
          self.appname = res;
        },
        error:function(data){
          if (data.status == 403) {
            alert("请求被拒绝,请登陆系统");
            window.location.href="/salt/login";
          }
        },
      });
    },
    getmvntype:function () {
      var self = this;
      reqwest({
        url:"api/salt/mvntype",
        type:"json",
        headers:Cookies.get('token')? {'Authorization': 'token ' + Cookies.get('token')}:{},
        method:"get",
        success:function(res){
          self.mvntype = res;
        },
        error:function(data){
          if (data.status == 403) {
            alert("请求被拒绝,请登陆系统");
            window.location.href="/salt/login";
          }
        },
      });
    },
    getmvnorder:function () {
      var self = this;
      reqwest({
        url:"api/salt/mvnorder",
        type:"json",
        headers:Cookies.get('token')? {'Authorization': 'token ' + Cookies.get('token')}:{},
        method:"get",
        success:function(res){
          self.mvnorder = res;
        },
        error:function(data){
          if (data.status == 403) {
            alert("请求被拒绝,请登陆系统");
            window.location.href="/salt/login";
          }
        },
      });
    },
    getserverinfo:function (id) {
      var self = this;
      this.selectall = "";
      reqwest({
        url:"api/salt/serverinfo/" + id,
        type:"json",
        headers:Cookies.get('token')? {'Authorization': 'token ' + Cookies.get('token')}:{},
        method:"get",
        success:function(res){
          self.server = res;
          self.checkedValue=[];
          self.result = [];
          self.showloading = 0;
          // self.defaultChecked();
        },
        error:function(data){
          if (data.status == 403) {
            alert("请求被拒绝,请登陆系统");
            window.location.href="/salt/login";
          }
        },
      });
    },
    findserver:function() {
      var self = this;
      var groupids=this.groupinfo.map(function(grp) {
        return grp.id;
      });
      reqwest({
        url:"api/salt/findserver",
        type:"json",
        method:"post",
        data:{
          groupid:groupids.toString(),
          ip:this.serverip,
        },
        success:function(res) {
          self.server=res;
        },
        error:function(data) {
          if (data.status == 404) {
            alert('IP地址不存在');
          }
        },
      });
    },
    getcommand:function() {
      var self = this;
      reqwest({
        url:"api/salt/commandlist",
        type:"json",
        method:"get",
        headers:Cookies.get('token')? {'Authorization': 'token ' + Cookies.get('token')}:{},
        success:function(res) {
          self.command = res;
        },
        error:function(data){
          if (data.status == 403) {
            alert("请求被拒绝,请登陆系统");
            window.location.href="/salt/login";
          }
        },
      });
    },
    sendcommand:function(){
      if (Number(this.showORnot) === 0){
        this.senddata();
      } else if (Number(this.showORnot) === 1)  {
        this.sendcustom();
      } else if (Number(this.showORnot) === 2)  {
        this.sendupdate();
      }
    },
    senddata:function() {
      var conTostr = this.checkedValue.toString();
      var command = this.radioValue;
      var self = this;
      if (conTostr.length === 0 || Number(this.radioValue) === 0) {
        alert("服务器IP和指令不能为空");
      }
      else {
        this.result = [];
        self.showloading = 1;
        this.butstatus = 'disabled';
        reqwest({
          url:'api/salt/result',
          type:'json',
          headers:Cookies.get('token')? {'Authorization': 'token ' + Cookies.get('token')}:{},
          method:'post',
          data:{
            serverlist: conTostr,
            command: command,
          },
          success:function(res){
            for (var i=0;i<res.length;i++) {
              res[i].result = res[i].result.split('\n');
            }
            self.result = res;
            self.butstatus = "";
          },
          error:function(data) {
            self.butstatus = "";
            self.showloading = 0;
            if (data.status == 403) {
              alert("请求被拒绝,请登陆系统");
              window.location.href="/salt/login";
            }
          }
        });
      }
    },
    sendcustom:function() {
      var conTostr = this.checkedValue.toString();
      var customorder = this.customorder;
      var arg1 = this.arg1.replace(/(^\s*)|(\s*$)/g, "");
      var arg2 = this.arg2;
      var code = this.code;
      var self = this;
      if (conTostr.length === 0 || customorder.length === 0 || code.length === 0 || arg1.length === 0 ) {
        alert("服务器IP,参数1和验证码不能为空");
      }
      else {
        this.result = [];
        self.showloading = 1;
        this.butstatus = 'disabled';
        reqwest({
          url:'api/salt/customorder',
          type:'json',
          headers:Cookies.get('token')? {'Authorization': 'token ' + Cookies.get('token')}:{},
          method:'post',
          data:{
            serverlist: conTostr,
            command: customorder,
            arg1: arg1,
            arg2: arg2,
            code: code,
          },
          success:function(res){
            for (var i=0;i<res.length;i++) {
              res[i].result = res[i].result.split('\n');
            }
            self.result = res;
            self.butstatus = "";
          },
          error:function(data){
            self.butstatus = "";
            self.showloading = 0;
            if (data.status == 401) {
              alert("认证码错误");
            } else if (data.status == 406) {
              alert("rm 指令禁止被使用");
            } else if (data.status == 403) {
              alert("请求被拒绝,请登陆系统");
              window.location.href="/salt/login";
            }
          }
        });
      }
    },
    sendupdate:function() {
      var conTostr = this.checkedValue.toString();
      var appname = this.appValue;
      var svnurl = this.svnurl.replace(/(^\s*)|(\s*$)/g, "");
      var command = this.mvnValue;
      var buildtype = this.typeValue;
      var code = this.code;
      var self = this;
      this.result = [];
      if (conTostr.length === 0 || Number(this.appValue) === 0 || Number(this.mvnValue) === 0 || Number(this.typeValue) === 0  || code.length === 0 || svnurl.length === 0) {
        alert("服务器IP和指令不能为空");
      }
      else {
        self.showloading = 1;
        this.butstatus = 'disabled';
        reqwest({
          url:'api/salt/updatecommand',
          type:'json',
          headers:Cookies.get('token')? {'Authorization': 'token ' + Cookies.get('token')}:{},
          method:'post',
          data:{
            serverlist: conTostr,
            appname:appname,
            svnurl:svnurl,
            buildtype:buildtype,
            buildcommand:command,
            code:code,
          },
          success:function(res){
            for (var i=0;i<res.length;i++) {
              res[i].result = res[i].result.split('\n');
            }
            self.result = res;
            self.butstatus = "";
          },
          error:function(data){
            self.showloading = 0;
            self.butstatus = "";
            if (data.status == 401) {
              alert("认证码错误");
            } else if (data.status == 406) {
              alert("rm 指令禁止被使用");
            } else if (data.status == 403) {
              alert("请求被拒绝,请登陆系统");
              window.location.href="/salt/login";
            }
          }
        });
      }


    },
    selectAll:function(){
      var serverlist = this.server;
      var self = this;
      if(this.checkedValue.length === 0){
        this.checkedValue = [];
        serverlist.forEach(function(item) {
          self.checkedValue.push(item.ip);
        });
        this.selectall = true;
      }else if (this.checkedValue.length === this.server.length ) {
        this.checkedValue =[];
        this.selectall= "";
      }else {
        this.checkedValue = [];
        serverlist.forEach(function(item) {
          self.checkedValue.push(item.ip);
        });
      }
    },
    defaultChecked:function() {
      var serverlist = this.server;
      if (serverlist.length == 1) {
        this.checkedValue = serverlist[0].ip;
      } else {
        this.checkedValue = [];
      }
    },
    showMore:function() {
      this.showloading = 0;
      this.showORnot = 1;
      this.radioValue = 0;
    },
    showUpdate:function() {
      this.showloading = 0;
      this.showORnot = 2;
      this.radioValue = 0;
      this.appValue = 0;
      this.mvnValue = 0;
      this.typeValue = 0;
    },
    findServer:function() {
      var servers = this.serverlist;

    }
  },
  computed:{
    filterId:function(){
      var serverlist = this.server;
      var self = this;
      var newList =serverlist.filter(function (a){
        return a.belong_to.name== self.selected;
      });
      return newList;
    },
    loadingOrNot:function() {
      if (this.result.length === 0) {
        return '  loading';
      } else {
        return '';
      }
    }
  },
  ready:function() {
    this.getgroup();
    this.getcommand();
    this.getappname();
    this.getmvntype();
    this.getmvnorder();
  }
});
