<style scoped>
  #userDetail{
    font-size: 18px;
  }
  .back{
    border:none;
    font-size: 18px;
  }
  .back span{
    display: inline-block;
    margin-left: 5px;
  }
  .firstBtn{
    margin-bottom: 20px;
  }
  .wrapper button{
    font-size: 18px;
    padding:15px 20px;
  }
  .passInterval{
    margin-bottom: 20px;
    line-height: 50px;
  }
  .passWrong{
    text-align: center;
    padding-right: 50px;
    position: absolute;
    color: #FF4949;
  }
  .dialog-footer{
    border-top: 2px solid #d8d8d8;
    padding-top: 20px;
  }
  .relatedPro{
    margin-bottom: 10px;
    line-height: 30px;
  }
  .changeComment{
    margin-bottom: 10px;
    line-height: 30px;
  }  
  .recordTable{
    width:80%;
    line-height: 50px;
    font-size: 18px;
    box-shadow: 0px 2px 4px 0px rgba(0,0,0,0.50);
    cursor: pointer;
  }
  .dialogPermiss{
    margin-top: 50px;
  }
</style>

<template>
  <div id="userDetail">
    <div class="firstBtn">
      <el-button class="el-icon-arrow-left back" @click="back"><span>返回</span></el-button>
    </div>
    <div class="block">
      <span class="wrapper">
        <el-button type="primary" @click="dialogChangeword = true">修改密码</el-button>
        <el-button type="primary" @click="dialogChangepermiss = true">修改权限</el-button>
        <el-button type="primary" @click="dialogRelatedperfect = true">关联项目</el-button>
        <el-button type="primary" @click="dialogChangecomment = true">修改备注</el-button>        
        <el-button type="danger" @click="freeze">冻结</el-button>
      </span>
    </div>
    <div>
      <table width="400" style="margin-bottom: 30px;margin-top: 30px">
        <tr height="40">
          <td>用户名</td>
          <td>{{info.user_name}}</td>
        </tr>
        <tr height="40">
          <td>状态</td>
          <td>{{info.state}}</td>
        </tr>
        <tr height="40">
          <td>角色</td>
          <td>{{info.user_type}}</td>
        </tr>
        <tr height="40">
          <td>项目</td>
          <td>{{info.projs}}</td>
        </tr>
        <tr height="40">
          <td>备注</td>
          <!-- <td><input type="text" style="border: none" id="comment_n" value="ffff"></td> -->
          <td>{{info.comment}}</td>
        </tr>
      </table>
    </div>
    <div>
      <h3 style="font-weight: normal">登录记录</h3>
      <el-table :data="loginRecord"  class="recordTable">
        <el-table-column prop="login_time" label="登录时间" style="width: 40%"></el-table-column>
        <el-table-column prop="ip" label="登录IP" style="width: 40%"></el-table-column>
      </el-table>
    </div>
    <el-dialog title="修改密码"  v-model="dialogChangeword">
      <el-row class="passInterval">
        <el-col :span="6">输入密码</el-col>
        <el-col :span="12">
          <el-input placeholder="请输入密码" type='password' v-model="pass"></el-input>
        </el-col>
      </el-row>
      <el-row class="passInterval">
        <el-col :span="6">确认密码</el-col>
        <el-col :span="12">
          <el-input placeholder="请确认密码" type='password' v-model="rePass"></el-input>
        </el-col>
      </el-row>

        <el-col :span="24" class="passWrong" v-if="showWrong">请输入相同的密码</el-col>

      <div slot="footer" class="dialog-footer">
        <el-button @click="exitPass">取 消</el-button>
        <el-button type="primary" @click="submitPass">确 定</el-button>
      </div>
    </el-dialog>
    <el-dialog title="修改角色" v-model="dialogChangepermiss" >
      <el-col :span="6">选择角色组</el-col>
      <el-col :span="12">
        <el-select v-model="value" placeholder="请选择" @change="permissSelected">
          <el-option
            v-for="item in options"
            :label="item.label"
            :value="item.value">
          </el-option>
        </el-select>
      </el-col>
      <div slot="footer" class="dialog-footer dialogPermiss">
        <el-button @click="exitPermiss">取 消</el-button>
        <el-button type="primary" @click="submitPermiss">确 定</el-button>
      </div>
    </el-dialog>
    <el-dialog title="关联项目" v-model="dialogRelatedperfect">
      <el-col :span="24" class="relatedPro">请选择关联的项目</el-col>

      <el-checkbox :indeterminate="isIndeterminate" v-model="checkAll" @change="handleCheckAllChange">全选</el-checkbox>

      <div style="margin: 15px 0;"></div>
      <el-checkbox-group v-model="checkedCities" @change="handleCheckedCitiesChange">      
        <el-checkbox v-for="city in selectProj" :label="city">{{city}}</el-checkbox>
<!--         <el-checkbox label="项目1"></el-checkbox>
        <el-checkbox label="项目2"></el-checkbox>
        <el-checkbox label="项目3"></el-checkbox>
        <el-checkbox label="项目4"></el-checkbox> -->
      </el-checkbox-group>
      <div slot="footer" class="dialog-footer">
        <el-button @click="exitRelated">取 消</el-button>
        <el-button type="primary" @click="submitRelated">确 定</el-button>
      </div>
    </el-dialog>
    <el-dialog title="修改备注" v-model="dialogChangecomment">
      <el-row class="passInterval">
        <el-col :span="6">输入备注</el-col>
        <el-col :span="12">
          <el-input placeholder="请输入备注" v-model="comment_c"></el-input>
        </el-col>
      </el-row>
      <div slot="footer" class="dialog-footer">
        <el-button @click="exitRelated">取 消</el-button>
        <el-button type="primary" @click="submitComment">确 定</el-button>
      </div>
    </el-dialog>    
  </div>
</template>
<script>
  import {mapActions} from 'vuex'
  export default{
    data () {
      return {
        loginRecord:[],
        // [{
        //   time:'2017-01-16 11:33',address:'116.119.118.20'
        // },{
        //   time:'2017-01-17 11:33',address:'116.119.118.21'
        // },{
        //   time:'2017-01-18 11:33',address:'116.119.118.22'
        // },{
        //   time:'2017-01-19 11:33',address:'116.119.118.23'
        // }],
        dialogChangeword:false,
        dialogChangepermiss:false,
        dialogRelatedperfect:false,
        dialogChangecomment:false,
        checkAll: false,
        checkedCities: [],
        isIndeterminate: false ,       
        pass:'',
        rePass:'',
        showWrong:false,
        checkList:[],
        info:'',
        comment_c:'',
        options:[{
          value:'超级管理员',
          label:'超级管理员'
        },{
          value:'管理员',
          label:'管理员'
        },{
          value:'商务',
          label:'商务'
        },{
          value:'客户',
          label:'客户'
        },
        // {
        //   value:'渠道',
        //   label:'渠道'
        // },
        ],
        value:'',
        selectProj:[],

        apiUrl_filter: 'http://120.27.131.91:8098/act_cnt/get_user_logintime_list?',
        apiUrl_pw: 'http://120.27.131.91:8098/act_cnt/change_passwd?',
        apiUrl_fr: 'http://120.27.131.91:8098/act_cnt/froze_accout?',
        apiUrl_role: 'http://120.27.131.91:8098/act_cnt/change_role?',
        apiUrl_projs: 'http://120.27.131.91:8098/act_cnt/get_projs?',
        apiUrl_change_projs: 'http://120.27.131.91:8098/act_cnt/change_related_project?',
        apiUrl_comment: 'http://120.27.131.91:8098/act_cnt/change_comment?',

        //apiUrl_filter: 'http://localhost:8099/act_cnt/get_user_logintime_list?',
        //apiUrl_pw: 'http://localhost:8099/act_cnt/change_passwd?',
        //apiUrl_fr: 'http://localhost:8099/act_cnt/froze_accout?',
        //apiUrl_role: 'http://localhost:8099/act_cnt/change_role?',
        //apiUrl_projs: 'http://localhost:8099/act_cnt/get_projs?',
        //apiUrl_change_projs: 'http://localhost:8099/act_cnt/change_related_project?',
        //apiUrl_comment: 'http://localhost:8099/act_cnt/change_comment?',
      }
    },
    methods:{
      ...mapActions(['logOut','disableLogin',]),
      toLogout(){
        this.logOut()
        this.disableLogin()
      },         
      back:function () {
        this.$router.push('/set/user')
      },
      freeze:function () {
        this.$confirm('冻结该用户将无法登录，是否冻结','冻结',{
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() =>{

          var apiUrl_local = this.apiUrl_fr + "user_name=" + this.info.user_name

          this.$http.jsonp(apiUrl_local,
              {
                  jsonp:'_cb_mine'
              }
              )
              .then(function(response) {
                  console.log("fdadafffffffff")
              }, function(response) {
                  console.log("my site para detail  filtering   JSON fucked")
              })

          this.$alert('冻结成功','冻结',{
            confirmButtonText: '确定',
          })
          // setTimeout(function(){
          //     //_this.id=_this.$store.state.login.info.id
          //     //_this.getCustomers_top5()
          //     //_this.getCustomers_mapdata()
          //     this.toLogout()()
          // },30)
          this.toLogout()
        }).catch(() =>{
          this.$message({
            type: 'info',
            message: '已取消删除'
          });
        })
      },
      submitPass:function () {
        if(this.rePass!==this.pass || this.pass =='' || this.rePass == ''){
          this.showWrong=true
        }else{
          this.dialogChangeword=false

          var apiUrl_local = this.apiUrl_pw + "passwd=" + this.pass + "&user_name=" + this.info.user_name

          this.$http.jsonp(apiUrl_local,
              {
                  jsonp:'_cb_mine'
              }
              )
              .then(function(response) {
                  console.log("fdadafffffffff")
              }, function(response) {
                  console.log("my site para detail  filtering   JSON fucked")
              })

          this.pass=''
          this.rePass=''
          this.showWrong=false

          this.$alert('密码修改成功,请重新登录','修改密码',{
            confirmButtonText: '确定',
          })
          this.toLogout()          
        }
      },
      exitPass:function () {
        this.dialogChangeword=false
        this.pass=''
        this.rePass=''
        if(this.showWrong==true){
          this.showWrong=false
        }else{
          return false
        }
      },
      submitRelated:function () {
        this.dialogRelatedperfect=false
        this.getCustomersFilter_change_projs()
      },
      exitRelated:function () {
        this.dialogRelatedperfect=false
      },
      submitComment:function () {
        this.dialogChangecomment=false
        
        var apiUrl_local = this.apiUrl_comment + "user_name=" + this.info.user_name +"&comment="+this.comment_c
        this.$http.jsonp(apiUrl_local,
            {
                jsonp:'_cb_mine'
            }
            )
            .then(function(response) {
                console.log("fdadafffffffff")
                // this.loginRecord = response.data.allData
                //this.tableData=this.allData.slice(0,7)
                //this.total=this.allData.length
                //this.currentPage = 1
                //this.pageSize = 7
                console.log("para detail filtering   not fucked")
                // console.log(this.countData)
                console.log("over")
            }, function(response) {
                console.log("my site para detail  filtering   JSON fucked")
            })         
      },
      exitComment:function () {
        this.dialogChangecomment=false
      },      
      submitPermiss:function () {
        this.dialogChangepermiss=false
        
        var apiUrl_local = this.apiUrl_role + "user_name=" + this.info.user_name +"&role="+this.value
        this.$http.jsonp(apiUrl_local,
            {
                jsonp:'_cb_mine'
            }
            )
            .then(function(response) {
                console.log("fdadafffffffff")
                // this.loginRecord = response.data.allData
                //this.tableData=this.allData.slice(0,7)
                //this.total=this.allData.length
                //this.currentPage = 1
                //this.pageSize = 7
                console.log("para detail filtering   not fucked")
                // console.log(this.countData)
                console.log("over")
            }, function(response) {
                console.log("my site para detail  filtering   JSON fucked")
            })        

      },
      exitPermiss:function () {
        this.dialogChangepermiss=false
      },
      permissSelected:function (value) {
        return  value
      },
      getCustomersFilter: function() {
          //var _msg=JSON.parse(sessionStorage.getItem('_obj'))
          // var username = "null"
          var apiUrl_local = this.apiUrl_filter + "user_name=" + this.info.user_name
          this.$http.jsonp(apiUrl_local,
              {
                  jsonp:'_cb_mine'
              }
              )
              .then(function(response) {
                  console.log("fdadafffffffff")
                  this.loginRecord = response.data.allData
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
      getCustomersFilter_projs: function() {
          //var _msg=JSON.parse(sessionStorage.getItem('_obj'))
          // var username = "null"
          var apiUrl_local = this.apiUrl_projs
          this.$http.jsonp(apiUrl_local,
              {
                  jsonp:'_cb_mine'
              }
              )
              .then(function(response) {
                  console.log("fdadafffffffff")
                  this.selectProj = response.data.allData
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
      getCustomersFilter_change_projs: function() {
          //var _msg=JSON.parse(sessionStorage.getItem('_obj'))
          // var username = "null"
          var apiUrl_local = this.apiUrl_change_projs + "arr_projs=" + this.checkedCities +"&user_name="+this.info.user_name
          this.$http.jsonp(apiUrl_local,
              {
                  jsonp:'_cb_mine'
              }
              )
              .then(function(response) {
                  console.log("fdadafffffffff")
                  // this.selectProj = response.data.allData
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
      handleCheckAllChange(event) {
        this.cityOptions = this.selectProj
        this.cities = this.selectProj
        this.checkedCities = event.target.checked ? this.cityOptions : [];
        this.isIndeterminate = false;

        alert(this.checkedCities)
      },
      handleCheckedCitiesChange(value) {
        this.cityOptions = this.selectProj
        this.cities = this.selectProj
        let checkedCount = value.length;
        this.checkAll = checkedCount === this.cities.length;
        this.isIndeterminate = checkedCount > 0 && checkedCount < this.cities.length;

        alert(this.checkedCities)

      }                  
    },
    created:function () {
      var _this=this      
      this.info=this.$store.state.project.message
      setTimeout(function(){
          //_this.id=_this.$store.state.login.info.id
          //_this.getCustomers_top5()
          //_this.getCustomers_mapdata()
          _this.getCustomersFilter()
          _this.getCustomersFilter_projs()
      },30)
      //console.log(this.info)
      //console.log(this.info.comment)
      //console.log(document.getElementById("comment_n"))
      //document.getElementById("comment_n").value=this.info.comment
    }
  }
</script>
