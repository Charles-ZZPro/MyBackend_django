<style scoped>
  .time{
    margin-bottom: 20px;
  }
  .countTable{
    line-height: 50px;
    font-size: 18px;
    box-shadow: 0px 2px 4px 0px rgba(0,0,0,0.50);
    cursor: pointer;
    width:80%;
    color: #475669
  }
</style>
<template>
  <div id="count">
    <div class="block time">
<!--       <el-date-picker v-model="timeSelect" type="daterange"></el-date-picker> -->
        <el-date-picker
          v-model="value"
          type="daterange"
          placeholder="选择日期范围" style="width: 300px">
        </el-date-picker>
    <el-button v-on:click="getCustomersFilter" class='filterData'>筛选</el-button>        
    </div>
    <el-table :data="countData" class="countTable" >
      <el-table-column prop="proj_name" label="项目" style="width: 20%"></el-table-column>
      <el-table-column prop="daily_active" label="新增日活" style="width: 20%"></el-table-column>
      <el-table-column prop="duli" label="新增独立用户" style="width: 20%"></el-table-column>
      <el-table-column prop="newAddcount" label="前台新增日活显示数" style="width: 20%">
        <template scope="scope">
          <el-col :span="16">
            <el-input  v-model="addInput" placeholder="请输入数字"></el-input>
          </el-col>
          <el-col :span="6" style="margin-left: 10px">
            <el-button type="success" >保存</el-button>
          </el-col>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>
<script>
  export default{
    data (){
      return{
        timeSelect:[new Date(2017,1,16),new Date(2017,1,19)],
        value:"",
        countData:
        [],
        // [
        //   {project:'项目1',newAdd:'12355',newAdduser:'12311'},
        //   {project:'项目2',newAdd:'7643',newAdduser:'12312'},
        //   {project:'项目3',newAdd:'6765',newAdduser:'6643'},
        //   {project:'项目4',newAdd:'75455',newAdduser:'12311'},
        // ]
        //apiUrl: 'http://localhost:8099/act_cnt/get_tongji_to_frontpage?proj_id=',
        apiUrl_filter: 'http://localhost:8099/act_cnt/get_tongji_to_frontpage?',
      }
    },
    methods:{
      getCustomersFilter: function() {
          //var _msg=JSON.parse(sessionStorage.getItem('_obj'))
          var username = "null"
          var apiUrl_local = this.apiUrl_filter + "user_name=" + username+"&value="+this.value
          this.$http.jsonp(apiUrl_local,
              {
                  jsonp:'_cb_mine'
              }
              )
              .then(function(response) {
                  this.countData = response.data.allData
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
