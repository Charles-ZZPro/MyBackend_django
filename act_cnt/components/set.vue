<style scoped>
  #set{
    font-size: 18px;
  }
  .setTitle a{
    display: inline-block;
    padding: 10px 40px;
    color: #475669;
    margin-bottom: 35px;
    font-size: 18px;
  }
  .setTitle-active{
    background-color: #d2dce6;
  }
</style>
<template>
  <div id="set">
    <div class="setTitle">
      <router-link to="/set/user" active-class="setTitle-active">用户管理</router-link>
      <router-link to="/set/role" active-class="setTitle-active">角色管理</router-link>
    </div>
    <div>
      <router-view></router-view>
    </div>
  </div>

</template>
<script>
  export default{
    data (){
      return{
      }
    },
    methods:{
    },
    mounted:function () {
      this.$router.push('/set/user')
    },
    beforeRouterEnter(to,from,next){
      console.log(to)
    }
  }
</script>
