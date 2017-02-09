<template>
  <div id="project">
    <el-breadcrumb separator=">" class="zhTitle">
      项目列表
    </el-breadcrumb>
    <ul class="zhProject">
      <li  v-for="(item,index) in items" @click="showName(index)" class="zh-project-detail">
        <router-link :to="'/project/'+index" tag="div">
          <h1>{{item.title}}</h1>
          <div>总计激活数：{{item.number}}</div>
        </router-link>
      </li>
    </ul>
  </div>
</template>
<style scoped>
  #project{
    color:  #475669;
    font-family: PingFangSC-Regular
  }
  .zhTitle{
    font-size: 14px;
  }
  .zh-project-detail{
    width:450px;
    height:200px;
    text-align: center;
    float: left;
    background: #EFF2F7;
    display: block;
    cursor: pointer;
    border: 1px solid #99A9BF;
    margin-right: 20px;
    box-shadow: 0px 2px 4px 0px rgba(0,0,0,0.50);
  }
  .zh-project-detail:hover{
    border-color: blue;
  }
  ul.zhProject{
    padding: 0;
  }
</style>
<script>
  import {mapActions} from 'vuex'
  export default{
    created: function() {
        this.getCustomers()
    },

    watch:{

    },

    data (){
      return {
        items:[

        ],
        // apiUrl: 'http://120.77.179.136:8099/act_cnt/get_active_totalnums'
        apiUrl: 'http://localhost:8099/act_cnt/get_active_totalnums'
      }
    },

    methods:{
      ...mapActions(['setInfo']),

      showName(str){
        var info=this.items[str]
        this.setInfo(info)
        // var obj={'title':this.items[str].title,'number':this.items[str].number,'id':this.items[str].id}

        // sessionStorage.setItem('_obj',JSON.stringify(obj))
        // var _msg=JSON.parse(sessionStorage.getItem('_obj'))
        // this.$bus.emit('showmsg')
      },

      // showName (str){
      //     var obj={'title':this.items[str].title,'number':this.items[str].number,'id':this.items[str].id}

      //     sessionStorage.setItem('_obj',JSON.stringify(obj))
      //     var _msg=JSON.parse(sessionStorage.getItem('_obj'))

      //     this.$bus.emit('showmsg')
      //     this.shareState.record.name=this.items[str].title
      //     this.shareState.record.number=this.items[str].number
      //     this.shareState.record.id=this.items[str].id


      // },

      activate (){
          store.dispatch('INCREMENT')
      },

      getCustomers: function() {

          this.$http.jsonp(this.apiUrl,
              {
                  jsonp:'_cb_mine'
              }
              )
              .then(function(response) {
                  //console.log(response)
                  this.items = response.data.tuple
                  //console.log("not fucked")
                  //console.log(this.items)
              }, function(response) {
                  //console.log("my site JSON fucked")
              })
      }

    }
  }
</script>
