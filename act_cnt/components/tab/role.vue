<style scoped>
  #role{
    font-size: 18px;
  }
  .roleTable{
    width:75%;
    line-height: 50px;
    font-size: 18px;
    box-shadow: 0px 2px 4px 0px rgba(0,0,0,0.50);
    cursor: pointer;
  }
  .roleBtn{
    font-size: 18px;
  }
  .dialog-footer{
    border-top: 2px solid #d8d8d8;
    padding-top: 20px;
  }
</style>
<template>
  <div id="role">
    <el-table :data="roleData" class="roleTable">
      <el-table-column prop="role" label="角色" style="width: 25%"></el-table-column>
      <el-table-column prop="menues" label="模块" style="width: 25%"></el-table-column>
      <el-table-column prop="handel" label="操作" style="width: 25%">
        <template scope="scope">
          <el-button type="text" class="roleBtn" @click="roleSet( scope.row)">设置</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog title="设置角色组" v-model="dialogRole">
      <h3 style="font-weight: normal">请选择该角色可访问的菜单</h3>
      <el-checkbox-group v-model="roleList">
        <el-checkbox v-for="role in selectRole" :label="role"></el-checkbox>
      </el-checkbox-group>
      <div slot="footer" class="dialog-footer">
        <el-button @click="exitRoleset">取 消</el-button>
        <el-button type="primary" @click="submitRoleset">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>
<script>
  export default{
    data (){
      return{
        roleData:[
          // {role:'超级管理员',model:'项目，统计，设置'},
          // {role:'管理员',model:'项目，统计，设置'},
          // {role:'商务',model:'项目，统计'},
          // {role:'客户',model:'项目'}
        ],
        dialogRole:false,
        roleList:[],
        selectRole:[],
        apiUrl_filter: 'http://localhost:8099/act_cnt/get_rolemenues_info?',
        }
    },
    methods:{
      roleSet:function (row) {
        this.dialogRole=true;
        this.selectRole=row.model.split("，")
      },
      exitRoleset:function () {
        this.dialogRole=false
        this.roleList=[]
      },
      submitRoleset:function () {
        this.dialogRole=false
      },
      getCustomersFilter: function() {
          //var _msg=JSON.parse(sessionStorage.getItem('_obj'))
          // var username = "null"
          var apiUrl_local = this.apiUrl_filter
          this.$http.jsonp(apiUrl_local,
              {
                  jsonp:'_cb_mine'
              }
              )
              .then(function(response) {
                  console.log("fdadafffffffff")
                  this.roleData = response.data.allData
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
    created:function () {
      var _this=this      
      // this.info=this.$store.state.project.message
      setTimeout(function(){
          //_this.id=_this.$store.state.login.info.id
          //_this.getCustomers_top5()
          //_this.getCustomers_mapdata()
          _this.getCustomersFilter()
      },30)
      //console.log(this.info)
      //console.log(this.info.comment)
      //console.log(document.getElementById("comment_n"))
      //document.getElementById("comment_n").value=this.info.comment
    }    ,
    watch:{
      roleList:function () {
        console.log(1)
      }
    }
  }
</script>
