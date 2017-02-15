<template>
  <header id="header">
    <el-row>
      <el-col :span="24">
        <div class="zh-h-title-l">
          <span>Tripics</span><span>运营后台</span>
        </div>
        <div class="zh-h-title-r">
          <span v-text='user'></span>
          <span>|</span>
          <button @click="toLogout" >退出</button>
        </div>
      </el-col>
    </el-row>
  </header>
</template>
<script>
  import {mapActions} from 'vuex'
  export default{
    computed:{
      user (){
        return this.$store.state.user.username
      }
    },
    methods:{
      ...mapActions(['logOut','disableLogin',]),
      toLogout(){
        this.logOut()
        this.disableLogin()
      },
      toLogin(){
        this.logIn()
      }
    },
    data (){
      return {
        user:{},
      }
    },

  }
</script>
<style scoped>
  *{
    margin: 0;
    padding: 0;
  }
  #header{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 60px;
    box-shadow: 0 2px 5px 0 rgba(0, 0, 0, 0.16), 0 2px 10px 0 rgba(0, 0, 0, 0.12);
    background-color: #324057;
    z-index: 100;
    font-family: PingFangSC-Semibold;
    color: #fff;
    padding: 0 20px;
    font-size: 18px;
  }
  .zh-h-title-l{
    height: 100%;
    line-height: 60px;
  }
  .zh-h-title-l span{
    display: inline-block;

  }
  .zh-h-title-l span:nth-child(1){
    font-weight: bolder;
    margin-right: 10px;
  }
  .zh-h-title-r{
    position: absolute;
    top:0;
    right:40px;
    line-height: 60px;
    font-size: 20px;
    font-weight: bolder;
  }
  button{
    border: none;
    font-size: 18px;
    color: #fff;
    background-color: #2f4256;
    font-weight: bolder;
    cursor: pointer;
  }
  button:hover{
    color: red;
  }

</style>
