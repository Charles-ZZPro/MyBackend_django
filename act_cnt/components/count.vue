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
  .zh-wenzi{
    display: inline-block;
  }
  .zh-select{
    display: inline-block;
    width: 180px
  }
  .zh-start{
    width: 120px
  }
</style>
<template>
  <div id="count">


    <div class="block time">
    <el-row :span='16'>
      <el-col :span='4' >
          起始:
          <el-date-picker
          v-model="value1"
          type="date"
          placeholder="选择日期"
          :picker-options="pickerOptions1" class='zh-start'>
          </el-date-picker> 
      </el-col>
      <el-col :span='4' >
        结束:
        <el-date-picker
        v-model="value2"
        type="date"
        placeholder="选择日期"
        :picker-options="pickerOptions1" class='zh-start'>
        </el-date-picker>
      </el-col>
      <el-col :span='6'>
        <span class='zh-wenzi'>选择项目:</span>
        <el-select v-model="value" placeholder="请选择" @change="proj_sel" class='zh-select'>
          <el-option
            v-for="item in selectProj"
            :label="item"
            :value="item" >
          </el-option>
        </el-select>
      </el-col>
      <el-col :span='2'>
        <el-button v-on:click="getCustomersFilter" >筛选</el-button>
      </el-col>
    </el-row>

      <!-- <span class="demonstration">起始:</span>
      <el-date-picker
        v-model="value1"
        type="date"
        placeholder="选择日期"
        :picker-options="pickerOptions1">
      </el-date-picker> 
      <span class="demonstration">&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</span>
      <span class="demonstration">结束:</span>    
      <el-date-picker
        v-model="value2"
        type="date"
        placeholder="选择日期"
        :picker-options="pickerOptions1">
      </el-date-picker>   

      <span class="demonstration">&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</span>
      <span class="demonstration">选择项目:</span>

        <el-select v-model="value" placeholder="请选择" @change="proj_sel" class='zh-select'>
          <el-option
            v-for="item in selectProj"
            :label="item"
            :value="item">
          </el-option>
        </el-select>
      <el-button v-on:click="getCustomersFilter" class='filterData'>筛选</el-button>   -->      
    </div>
    <el-table :data="countData" class="countTable" >
      <el-table-column prop="sub_channel_name" label="项目" style="width: 20%"></el-table-column>

      <el-table-column prop="date" label="日期" style="width: 20%"></el-table-column>      date
      <el-table-column prop="daily_active" label="日活跃" style="width: 20%"></el-table-column>
      <!-- <el-table-column prop="total_active" label="总日活" style="width: 20%"></el-table-column> -->
      <el-table-column prop="duli" label="新增独立用户" style="width: 20%"></el-table-column>
      <el-table-column prop="total_duli" label="总独立用户" style="width: 20%"></el-table-column>            
      <el-table-column prop="newAddcount" label="前台新增日活跃显示数" style="width: 20%">
        <template scope="scope">
          <el-col :span="5">
            <el-input  v-model="addInput" placeholder="请输入数字"></el-input>
          </el-col>
          <el-col :span="1" style="margin-left: 10px">
            <el-button type="success" >保存</el-button>
          </el-col>
        </template>
      </el-table-column>
    </el-table>
    <br />
    <el-row class="zh-page">
      <el-col :span="20">
        <el-pagination
          align="right"
          @current-change="handleCurrentChange"
          :current-page="1"
          :page-size="pageSize"
          layout="total,prev, pager, next, jumper"
          :total="total">
        </el-pagination>
      </el-col>
    </el-row>    
  </div>
</template>
<script>
  export default{
    data (){
      return{
        timeSelect:[new Date(2017,1,16),new Date(2017,1,19)],
        value:"",
        value1:"",
        value2:"",
        total:0,
        selectProj:
        [],
        value:"",
        countData:
        [],
        allData:
        [],
        pickerOptions0: {
          disabledDate(time) {
            return time.getTime() < Date.now() - 8.64e7;
          }
        },
        pickerOptions1: {
          shortcuts: [{
            text: '今天',
            onClick(picker) {
              picker.$emit('pick', new Date());
            }
          }, {
            text: '昨天',
            onClick(picker) {
              const date = new Date();
              date.setTime(date.getTime() - 3600 * 1000 * 24);
              picker.$emit('pick', date);
            }
          }, {
            text: '一周前',
            onClick(picker) {
              const date = new Date();
              date.setTime(date.getTime() - 3600 * 1000 * 24 * 7);
              picker.$emit('pick', date);
            }
          }]
        },        
        // [
        //   {project:'项目1',newAdd:'12355',newAdduser:'12311'},
        //   {project:'项目2',newAdd:'7643',newAdduser:'12312'},
        //   {project:'项目3',newAdd:'6765',newAdduser:'6643'},
        //   {project:'项目4',newAdd:'75455',newAdduser:'12311'},
        // ]

        apiUrl_filter: 'http://120.27.131.91:8099/act_cnt/get_tongji_to_frontpage?', 
        apiUrl_filter_proj: 'http://120.27.131.91:8099/act_cnt/get_tongji_to_frontpage_proj?',  
        apiUrl_projs: 'http://120.27.131.91:8099/act_cnt/get_projs?', 
        //apiUrl_filter: 'http://localhost:8099/act_cnt/get_tongji_to_frontpage?', 
        //apiUrl_filter_proj: 'http://localhost:8099/act_cnt/get_tongji_to_frontpage_proj?', 
        //apiUrl_projs: 'http://localhost:8099/act_cnt/get_projs?',
      }
    },
    methods:{
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
      getCustomersFilter: function() {
          //var _msg=JSON.parse(sessionStorage.getItem('_obj'))
          //alert(this.value1)
          if ((this.value1=="")&&(this.value2=="")){
            alert("请选择起始日期和结束日期")
          }
          else if (this.value1==""){
            alert("请选择起始日期")
          }
          else if (this.value2==""){
            alert("请选择结束日期")
          }
          else{
            var username = "WX"
            if(this.value==""){
              var apiUrl_local = this.apiUrl_filter + "user_name=" + username+"&value1="+this.value1+"&value2="+this.value2+"&proj="+this.value
            }
            else{
              var apiUrl_local = this.apiUrl_filter_proj + "user_name=" + username+"&value1="+this.value1+"&value2="+this.value2+"&proj="+this.value
            }            
            this.$http.jsonp(apiUrl_local,
                {
                    jsonp:'_cb_mine'
                }
                )
                .then(function(response) {
                    this.allData = response.data.allData;
                    //alert(this.countData)
                    if ((this.allData ==[])||(this.allData =="")){
                      alert("选定日期范围内无记录")
                    }
                    //this.tableData=this.allData.slice(0,7)
                    //this.total=this.allData.length
                    //this.currentPage = 1
                    //this.pageSize = 7
                    this.countData=this.allData.slice(0,7)
                    this.total=this.allData.length
                    //alert(this.total)
                    this.currentPage = 1
                    this.pageSize = 7                    
                    console.log("para detail filtering   not fucked")
                    console.log(this.countData)
                    console.log("over")
                }, function(response) {
                    console.log("my site para detail  filtering   JSON fucked")
                })
            if(this.value1=="first"){
              this.value1=""
              this.value2=""
            }
          }
      },  
      getCustomersFilter_projs_proj: function() {
          //var _msg=JSON.parse(sessionStorage.getItem('_obj'))
          //alert(this.value1)
          if ((this.value1=="")&&(this.value2=="")){
            alert("请选择起始日期和结束日期")
          }
          else if (this.value1==""){
            alert("请选择起始日期")
          }
          else if (this.value2==""){
            alert("请选择结束日期")
          }
          else{
            var username = "WX"
            var apiUrl_local = this.apiUrl_filter + "user_name=" + username+"&value1="+this.value1+"&value2="+this.value2+"&proj="+this.value
            this.$http.jsonp(apiUrl_local,
                {
                    jsonp:'_cb_mine'
                }
                )
                .then(function(response) {
                    this.allData = response.data.allData;
                    //alert(this.countData)
                    if ((this.allData ==[])||(this.allData =="")){
                      alert("选定日期范围内无记录")
                    }
                    //this.tableData=this.allData.slice(0,7)
                    //this.total=this.allData.length
                    //this.currentPage = 1
                    //this.pageSize = 7
                    this.countData=this.allData.slice(0,7)
                    this.total=this.allData.length
                    //alert(this.total)
                    this.currentPage = 1
                    this.pageSize = 7                    
                    console.log("para detail filtering   not fucked")
                    console.log(this.countData)
                    console.log("over")
                }, function(response) {
                    console.log("my site para detail  filtering   JSON fucked")
                })
            if(this.value1=="first"){
              this.value1=""
              this.value2=""
            }
          }
      },        
      getCustomersFilter_put_newaddDA: function() {
          //var _msg=JSON.parse(sessionStorage.getItem('_obj'))
          // var username = "null"
          var apiUrl_local = this.apiUrl_change_projs + "user_name=" + this.info.user_name
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
      handleCurrentChange(val) {
        this.currentPage = val;
        var endCount=val*this.pageSize
        var startCount=this.pageSize*(val-1)
        this.countData=this.allData.slice(startCount,endCount)
      },
      proj_sel:function (value) {
        return  value
      }
    },
    created:function(){
      var _this=this
        setTimeout(function(){
            //_this.id=_this.$store.state.login.info.id
            //_this.getCustomers_top5()
            //_this.getCustomers_mapdata()
             _this.value1 = "first"
             _this.value2 = "first"
            //alert(_this.value1)
            _this.getCustomersFilter()
            _this.getCustomersFilter_projs()
        },30)
    }    
  }
</script>
