var vm = new Vue({
  el:"#app",
  data:{
    loginfo:[],
    count:0,
    num:15,
  },
  methods:{
    getLog:function(){
      var self = this;
      reqwest({
        url:"/api/salt/log",
        type:"json",
        headers:Cookies.get("token")? {"Authorization": "token " + Cookies.get("token")}:{},
        method:"get",
        success:function(resp){
          self.loginfo = resp;
          self.count = self.loginfo.length;
        },
        error:function(data) {
          if (data.status === 403) {
            alert("无权限获取改数据");
          }
        }
      });
    },
    moreClick:function(){
      if (this.num + 15 < this.count) {
        this.num +=15;
      } else {
        this.num = this.count;
      }
    },
  },
  computed:{
    pagin:function() {
      var newlist = [];
      var num = this.num;
      if (num < this.loginfo.length) {
        for (var i=0;i<num;i++) {
          newlist[i] = this.loginfo[i];
          document.getElementById("bh2").style.cursor="pointer";
          document.getElementById("bh2").style.color="rgb(74, 140, 254)";
          document.getElementById("bh2").onmouseover=function(){
            this.style.color="red";
          };
          document.getElementById("bh2").onmouseout=function(){
            this.style.color="rgb(74, 140, 254)";
          };
        }
      } else if (num === this.loginfo.length || num > this.loginfo.length ) {
        newlist = this.loginfo;
        document.getElementById("bh2").style.cursor="default";
        document.getElementById("bh2").style.color="rgb(163, 170, 187)";
        document.getElementById("bh2").onmouseover=function(){
          this.style.color="rgb(163, 170, 187)";
        };
        document.getElementById("bh2").onmouseout=function(){
          this.style.color="rgb(163, 170, 187)";
        };
      }
      return newlist;
    }
  },
  filters:{
    dateFormat:function(datetime){
      var date = new Date(datetime);
      var newdate="";
      var year =date.getFullYear();
      var month = date.getMonth()+1;
      var day = date.getDate();
      var hour = date.getHours();
      var minute= date.getMinutes();
      var second= date.getSeconds();
      function addNum (num) {
        if (num >=10) {
          return num;
        }
        else {
          return '0' + num;
        }
      }
      newdate = year + '-' + addNum(month) + '-' + addNum(day) + ' ' + addNum(hour) + ':' + addNum(minute) + ':' + addNum(second);
      return newdate;
    }
  },
  ready:function(){
    this.getLog();
  },
});
