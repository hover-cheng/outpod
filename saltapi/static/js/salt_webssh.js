var vm = new Vue({
  el:"#terminal",
  data:{
      last_command:'\r\n',
      command: '',
      message:'',
      result: '',
      cols: '',
      rows: '',
      upload: '',
      upfilename: '',
      formdata: '',
      chatSocket: '',
      defaultTheme : {
        foreground: "#ffffff",
        background: "#1b212f",
        cursor: "#ffffff",
        selection: "rgba(255, 255, 255, 0.3)",
        black: "#000000",
        brightBlack: "#808080",
        red: "#ce2f2b",
        brightRed: "#f44a47",
        green: "#00b976",
        brightGreen: "#05d289",
        yellow: "#e0d500",
        brightYellow: "#f4f628",
        magenta: "#bd37bc",
        brightMagenta: "#d86cd8",
        blue: "#1d6fca",
        brightBlue: "#358bed",
        cyan: "#00a8cf",
        brightCyan: "#19b8dd",
        white: "#e5e5e5",
        brightWhite: "#ffffff",
      },
    },
  methods: {
    getFile:function() {
      this.upfilename = event.target.files[0];
    },
    uploadFile:function() {
      this.formdata = new FormData();
      // this.upfilename = document.getElementById('input_upload').files[0];
      this.formdata.append('filename', this.upfilename);
      this.chatSocket.send(this.formdata);
      // axios.post(window.location.pathname, formData).then(function(res) {console.log('ok');});
    },
    openFile:function() {
      var upload =  document.getElementById("input_upload");
      upload.click();
    },
    getvalue: function(name) {
      var reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
      var r = window.location.search.substr(1).match(reg);
      if (r != null) return unescape(r[0].split('=')[1]);
      return null;
    },
    isIp: function(value) {
      var reg = /(2(5[0-5]{1}|[0-4]\d{1})|[0-1]?\d{1,2})(\.(2(5[0-5]{1}|[0-4]\d{1})|[0-1]?\d{1,2})){3}/i;
      return reg.test(value);
    },
    sshclient: function(serveradd) {
      var _this = this;
      // Terminal.applyAddon(attach);
      // Terminal.applyAddon(fit);
      // Terminal.applyAddon(fullscreen);
      this.chatSocket = new WebSocket('ws://127.0.0.1:8000' +'/salt_ssh/?' + serveradd);
      var term = new Terminal({
        fontSize: 18,
        cursorStyle: 'bar',
        bellStyle: "sound",
        rows: this.rows,
        cols: this.cols,
        // rendererType: "canvas", //渲染类型
        // convertEol: true, //启用时，光标将设置为下一行的开头
        scrollback:100,//终端中的回滚量
        // disableStdin: false, //是否应禁用输入。
        // cursorStyle: 'underline', //光标样式
        cursorBlink: true, //光标闪烁
        theme: this.defaultTheme
      });
      term.open(document.getElementById('#terminal'));
      // term.toggleFullScreen(true);
      term.focus();
      this.chatSocket.binaryType='arraybuffer';
      this.chatSocket.onopen = function() {
      };
      this.chatSocket.addEventListener('message', function(e){
        _this.result = JSON.parse(e.data).message;
        if (_this.result.split('\r\n')[0] == _this.last_command) {
          _this.result = _this.result.substring(_this.result.indexOf('\r\n'), _this.result.length);
        }
        term.write(_this.result);
      });
      term.on('key', function(key, ev) {
        var printable = !ev.altKey && !ev.altGraphKey && !ev.ctrlKey && !ev.metaKey;
        if (ev.keyCode ===13) {
          if (_this.command == 'rz') {
            _this.openFile();
          } else {
            _this.chatSocket.send(_this.command + '\n');
            if (_this.command !='') {
              _this.last_command = _this.command;
            }
            _this.command = "";
          }
        } else if (ev.keyCode ===8) {
          _this.command = _this.command.slice(0, -1);
          if (term._core.buffer.x > _this.result.split('\r\n')[_this.result.split('\r\n').length -1].length) {
            // 输入删除键
            term.write('\b \b');
          }
        } else if (ev.ctrlKey && ev.keyCode == 67)  {
          // 发送 ctrl + c 指令
          _this.chatSocket.send('\x03');
        } else if (ev.keyCode == 27)  {
          // 发送 esc 指令(ASCII码中的十六进制)
          _this.chatSocket.send('\x1B');
        } else if (printable) {
          if (key == 'i' && _this.last_command.split(' ')[0] == 'vim') {
            _this.chatSocket.send(key);
          } else {
          _this.command += key;
          term.write(key);
        }
        }
      });
    },
  },
  mounted:function() {
    this.cols = parseInt(document.documentElement.clientWidth/9.7,10);
    this.rows = parseInt(document.documentElement.clientHeight/20,10);
    var hostip = this.getvalue("ipadd");
    if (this.isIp(hostip)) {
      this.sshclient(hostip);
    } else {
      alert("IP address is not legal...");
    }
  },
  watch:{
    upfilename:function(val) {
      this.uploadFile();
    },
  },
});
