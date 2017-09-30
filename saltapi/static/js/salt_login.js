var vm = new Vue({
  el:"#app",
  data:{
    username:"",
    password:"",
  },
  methods:{
    logIn:function() {
      var self = this;
      var username = this.username;
      var password = this.password;
      if (this.username.length === 0 || this.password.length ===0) {
        alert("用户名和密码不能为空");
      } else {
        reqwest({
          url:"/api/token-auth",
          type:"json",
          method:"post",
          data:{
            username:this.username,
            password:this.password,
          },
          success:function(resp) {
            // Cookies.set('token',resp.token,{expires: 1/24}); //expires: 1/24表示过期时间为二十四分之一天及1个小时
            // Cookies.set('username',self.username,{expires: 1/24});
            Cookies.set('token',resp.token);
             Cookies.set('username',self.username);
            window.location.href="../salt";
          },
          error:function(data) {
            if (data.status === 400) {
              alert("用户名或密码错误");
            }
          }
        });
      }
    }
  }
});
