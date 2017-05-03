<template>
  <div id="login">
    <el-row >
      <el-col :span="24" class="zh-title zh-title-h1"><h1>Tripics</h1></el-col>
      <el-col :span="24" class="zh-title-h2 "><h2>运营系统</h2></el-col>
      <el-col :span="8" class="zh-loginName">用户名</el-col>
      <el-col :span="8" class="zh-loginInput">
        <el-input placeholder="请输入用户名" v-model="nameInput"  autofocus="autofocus"></el-input>
      </el-col>
      <el-col :span="8" class="zh-loginName">密码</el-col>
      <el-col :span="8" class="zh-loginInput">
        <el-input placeholder="请输入密码" type='password' v-model="passInput"> </el-input>
      </el-col>
      <el-col :span="24" class="zh-showWrong" v-if="showWrong">
          用户密码错误
      </el-col>
      <el-col :span="24">
        <el-button :plain="true" class="zh-loginBtn" @click="toSubmit"><span>登录</span></el-button>
      </el-col>
    </el-row>
  </div>
</template>
<script>
  import {mapActions} from 'vuex'
  export default{
        created: function() {
            this.getCustomers()
        },
    methods: {


      getCustomers: function() {
          // $.ajax({
          //     url: this.apiUrl,
          //     dataType: "jsonp",
          //     jsonp: "callback",
          //     success: function(data) {
          //         this.item = data.tuple;
          //     }
          // })

          this.$http.jsonp(this.apiUrl,
              {
                  jsonp:'_cb_mine'
              }
              )
              .then(function(response) {
                  //console.log(response)

                  this.user_pass = response.data.tuple
                  //console.log("not fucked")

              }, function(response) {

                  //console.log("my site JSON fucked")
              })
      },

      ...mapActions(['logIn','enableLogin','logIn']),
      toSubmit() {

          //var _user=JSON.parse(sessionStorage.getItem('user'));
          //var _userName=_user.name;
          //var _passWord=_user.password;

          //if(this.nameInput == _userName && this.passInput ==_passWord){
          var inputnp = this.nameInput + this.passInput
          //inputnp_js = "{"+"}"

          if (this.user_pass.indexOf(inputnp) >= 0 && inputnp !='') {
              //console.log(this.nameInput)


              //var user={'name':this.nameInput,'password':this.passInput}

              //sessionStorage.setItem('user',JSON.stringify(user))

              //this.$router.push('/home/project')
              //this.$store.state.user.name = this.nameInput

            var apiUrl_put_logintime_fi = this.apiUrl_put_logintime + "?user_name=" + this.nameInput
            this.$http.jsonp(apiUrl_put_logintime_fi,
              {
                  jsonp:'_cb_mine'
              })
              .then(function(response){
                // 响应成功回调
              }, function(response){
                // 响应错误回调
              });           

            this.enableLogin();
            this.logIn(this.nameInput)
            this.$router.replace({path: '/project'});
              this.$message({
                  showClose: true,
                  message:'登录成功'
              })

          }else{
                    this.showWrong=true;


         }
      }
    },
      data (){
      return {
        nameInput:'',
        passInput:'',
        user_pass:'',
        apiUrl:'http://120.27.131.91:8098/act_cnt/get_user_info',
        apiUrl_put_logintime:'http://120.27.131.91:8098/act_cnt/put_logintime',
        //apiUrl:'http://localhost:8099/act_cnt/get_user_info',
        //apiUrl_put_logintime:'http://localhost:8099/act_cnt/put_logintime',
        showWrong:false
      }
    },
  }
</script>
<style scoped>
  body,div,dl,dt,dd,ul,ol,li,h1,h2,h3,h4,h5,h6,pre,code,form,fieldset,
  legend,input,button,textarea,p,blockquote,th,td { margin:0; padding:0; }
  #login{
    z-index: 101;
    width:780px;
    height: 438px;

    position:fixed;
    left: 50%;
    top: 50%;
    margin-left: -390px;
    margin-top: -219px;
    background: #324057;
    box-shadow: 0px 2px 4px 0px rgba(0,0,0,0.50);
    border-radius: 2px;
    text-align: center;
    padding: 20px;
    color: #fff;
  }
  .zh-title{
    margin-bottom: 10px;
  }
  .zh-title-h1{
    margin-top: 50px;
    font-size: 25px;
  }
  .zh-title-h2{
    margin-bottom: 50px;
  }
  .zh-loginName{
    text-align: right;
    font-size: 16px;
    line-height: 30px;
    margin-bottom: 30px;
  }
  .zh-loginInput{
    margin-left: 42px;
    margin-bottom: 30px;
    background: #FFFFFF;
    border-radius: 4px;
    outline: none;
  }
  .zh-showWrong{

    position: absolute;
    bottom: 20px;
    font-family: .PingFangSC-Regular;
    font-size: 12px;
    color: #FF4949;
    letter-spacing: 0px;
  }
  .zh-loginBtn{
    width: 104px;
    height: 40px;
    background-color: #20A0FF;
    border: none;
    color: #fff;
    position: relative;
    bottom: -40px;
    border-radius: 4px;
  }

</style>
