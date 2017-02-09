<template>
  <div id="nav">
    <ul class="nav-left">
      <li class="nav-item" v-for="(item,index) in items ">
        <router-link :to="'/'+item.ad" tag="div" active-class="zh-actived">{{item.name}}</router-link>
      </li>
    </ul>
  </div>
</template>
<script>
  export default{
    data (){
      return {
        items:[
          {name:'项目',ad:'project'},
          {name:'统计',ad:'count'},
          {name:'设置',ad:'set'}
        ]
      }
    }
  }
</script>
<style scoped>
  #nav{
    position: fixed;
    top:70px;
    bottom:0;
    left:0;
    background-color:  #EFF2F7;
    overflow-y: auto;
    z-index: 15;
    font-family:.PingFangSC-Regular;
    font-size: 14px;
    color: #475669;
    letter-spacing: 0px;


  }
  .nav-left {
    width:200px;
    height: 56px;
    line-height: 56px;
    text-align: center;
    padding: 0;
  }
  .nav-item{
    cursor: pointer;
  }
  .zh-actived{
    background:#d2dce6;

  }

</style>
