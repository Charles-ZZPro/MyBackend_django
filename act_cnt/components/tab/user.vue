<style scoped>
  #userSet{
    font-size: 18px;
  }
  .userSearch{
    width:350px;
    margin-bottom: 35px;
    font-size: 18px;

  }
  .userTable{
    width: 75%;
    cursor: pointer;
    font-size: 18px;
    line-height: 50px;
    box-shadow: 0px 2px 4px 0px rgba(0,0,0,0.50);
  }
</style>

<template>
  <div id="userSet">
    <el-input placeholder="请输入内容" v-model="search" class="userSearch">
      <template slot="prepend">用户名</template>
      <el-button v-on:click="getCustomersFilter" slot="append" icon="search" class='filterData'></el-button>
    </el-input>
    <el-table :data="tableData" border class="userTable" style="width: 75%;cursor: pointer ;font-size: 18px;line-height: 50px" @row-click="toDetail">
      <el-table-column prop="user_name" label="用户名" style="width:25%" ></el-table-column>
      <el-table-column prop="last_login_time" label="最后登录时间" style="width:25%"></el-table-column>
      <el-table-column prop="user_type" label="角色" style="width:25%"></el-table-column>
    </el-table>
  </div>
</template>

<script>
  import {mapActions} from 'vuex'
  export default{
    data (){
      return{
        search:'',
        apiUrl_filter: 'http://localhost:8099/act_cnt/get_user_info_list?',
        tableData:[],
        // [{
        //   name:'null',
        //   time:'2017-01-18',
        //   role:'管理员'
        // },
        //   {
        //     name:'slient',
        //     time:'2017-01-17',
        //     role:'用户'
        //   },
        //   {
        //     name:'eric',
        //     time:'2017-01-18',
        //     role:'管理员'
        //   }],
      }
    },
    methods:{
      ...mapActions(['setMes']),
      toDetail:function (row) {
        this.$router.push('/set/user/'+row.user_name)
        this.setMes(row)
      },
      getCustomersFilter: function() {
          //var _msg=JSON.parse(sessionStorage.getItem('_obj'))
          var username = "WX"
          var apiUrl_local = this.apiUrl_filter + "user_name=" + username+"&value="+this.search
          this.$http.jsonp(apiUrl_local,
              {
                  jsonp:'_cb_mine'
              }
              )
              .then(function(response) {
                  console.log("fdadafffffffff")
                  this.tableData = response.data.allData
                  //this.tableData=this.allData.slice(0,7)
                  //this.total=this.allData.length
                  //this.currentPage = 1
                  //this.pageSize = 7
                  console.log("para detail filtering   not fucked")
                  console.log(this.countData)
                  console.log("over")
              }, function(response) {
                  console.log("my site para detail  filtering   JSON fucked")
              })
      },       
    },
    created:function(){
      var _this=this
        setTimeout(function(){
            //_this.id=_this.$store.state.login.info.id
            //_this.getCustomers_top5()
            //_this.getCustomers_mapdata()
            _this.getCustomersFilter()
        },30)
    }   
  }
</script>
