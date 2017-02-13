<template>
  <div id="detail">
    <el-breadcrumb separator=">" class="zh-title">
      <el-breadcrumb-item :to="{ path: '/project' }" >项目列表</span></el-breadcrumb-item>
      <el-breadcrumb-item >{{message.title}}</el-breadcrumb-item>
      <el-breadcrumb-item >{{extraMsg}}</el-breadcrumb-item>
    </el-breadcrumb>
    <el-row class="zh-number">
      <el-col :span="24"  >
        总计激活数：<span v-text="message.number"></span>
      </el-col>
    </el-row >
    <el-row class="zh-map">
      <el-col :span="14">
        <charts :options="chart" class="chart"></charts>
      </el-col>
      <div class="countTable">Top5 活跃排行</div>
      <el-col :span="8" id="wordTable">
        <el-table :data="mapData" style="width: 100%;
        box-shadow: 0px 2px 4px 0px rgba(0,0,0,0.50);line-height: 60px">
          <el-table-column prop="name" label="国家" ></el-table-column>
          <el-table-column prop="value" label="总数" ></el-table-column>
          <el-table-column prop="percent" label="占比" ></el-table-column>
        </el-table>
      </el-col>
    </el-row>
    <el-row class="zh-date">
      <el-col :span="24">
        <el-date-picker
          v-model="value"
          type="daterange"
          placeholder="选择日期范围" style="width: 300px">
        </el-date-picker>
        <el-button v-on:click="getCustomersFilter" class='filterData'>筛选</el-button>
      </el-col>
    </el-row>
    <el-table :data="tableData" border style="width: 80%" class="zh-table">
      <el-table-column prop="date" label="日期" style="width:20%"></el-table-column>
      <el-table-column prop="activated_num" label="当日激活数" style="width:20%"></el-table-column>
      <el-table-column prop="addup_num" label="累计激活数" style="width:20%"></el-table-column>
      <el-table-column prop="lively_num" label="当日活跃数" style="width:20%"></el-table-column>
    </el-table>
    <el-row class="zh-page">
      <el-col :span="24">
        <el-pagination
          @current-change="handleCurrentChange"
          :current-page="1"
          :page-size="pageSize"
          layout="prev, pager, next, jumper"
          :total="total">
        </el-pagination>
      </el-col>
    </el-row>
  </div>
</template>
<style scoped>
  #detail{
    font-family: PingFangSC-Regular;
    font-size: 14px;
    color: #475669;
    letter-spacing: 0px;
  }
  .zh-title{
    font-size: 14px;
  }
  .zh-number{
    margin-top: 20px;
    color: #1F2D3D;
  }
  .zh-table{
    cursor: pointer;
    box-shadow: 0px 2px 4px 0px rgba(0,0,0,0.50);
    line-height: 60px;
  }
  #wordTable{
    cursor: pointer;
  }
  .chart{
    height:400px!important;
    width:700px!important;
    background-color: #d8d8d8;
  }
  .countTable{
    text-align: center;
    padding-right: 160px;
    margin-bottom: 20px;
    margin-top: 50px;
  }
  .zh-date{
    margin:10px 0 ;
  }
  .zh-page{
    text-align: right;
    margin-top: 10px;
    margin-right: 150px;
  }
  .filterData{
    background: #fff;
    border: 1px solid #ccc;
    border-radius: 5px;
    margin-left: 20px;
    height: 35px;
  }
  .filterData:hover{
    color: red;
    border:1px solid red;
  }
</style>
<script>
    import {mapState} from 'vuex'
    import {mapGetters} from 'vuex'
  import ECharts from 'vue-echarts/components/ECharts.vue'
  import '../../node_modules/vue-echarts/dist/world'
  export default{
    data (){
      return {
        message:'',
        extraMsg:'统计数据',
        chart:{
          tooltip : {
            trigger: 'item',
            formatter : function (params) {
              return params.seriesName + '<br/>' + params.name + ' : ' + params.value;
            }
          },
          toolbox: {
            show : true,
            orient : 'vertical',
            left: 'right',
            top: 'center',

          },
          visualMap: {
            type: 'continuous',
            min: 0,
            max: 300000,
            text:['High','Low'],
            realtime: false,
            calculable : true,
            color: ['orangered','yellow','lightskyblue']
          },
          series : [
            {
              name:'Daily active number',
              type: 'map',
              mapType: 'world',
              roam: true,
              itemStyle:{
                emphasis:{label:{show:true}}
              },
              data:[]
            }
          ]
        },
        mapData:[],
        value: '',
        tableData:[],
        allData:[],
        currentPage:1,
        total:0,
        pageSize:7,

        //apiUrl: 'http://120.77.179.136:8099/act_cnt/get_active_dailynums?proj_id=',
        //apiUrl_filter: 'http://120.77.179.136:8099/act_cnt/get_active_dailynums_filter?proj_id=',
        //apiUrl_top5: 'http://120.77.179.136:8099/act_cnt/get_top5_lively_country?proj_id=',
        //apiUrl_mapdata: 'http://120.77.179.136:8099/act_cnt/get_map_data?proj_id=',
        apiUrl: 'http://localhost:8099/act_cnt/get_active_dailynums?proj_id=',
        apiUrl_filter: 'http://localhost:8099/act_cnt/get_active_dailynums_filter?proj_id=',
        apiUrl_top5: 'http://localhost:8099/act_cnt/get_top5_lively_country?proj_id=',
        apiUrl_mapdata: 'http://localhost:8099/act_cnt/get_map_data?proj_id=',        
        name:'',
        number:'',
        id:'',
      }
    },
    components:{'charts':ECharts},
    computed:{
      message (){
        return this.$store.state.login.info
      },
    },
    /*created:function () {
      this.message=this.$store.state.login.info
    },*/
    methods:{
	    getCustomers: function() {
	        var apiUrl_local = this.apiUrl + this.id
	        this.$http.jsonp(apiUrl_local,
	            {
	                jsonp:'_cb_mine'
	            }
	            )
	            .then(function(response) {
	                this.allData = response.data.allData
                  this.tableData=this.allData.slice(0,7)
                  this.total=this.allData.length
      		        this.currentPage = 1
      			      this.pageSize = 7
	            }, function(response) {
	                console.log("my site para detail JSON fucked")
	            })
	    },
      getCustomers_top5: function() {
          var apiUrl_local = this.apiUrl_top5 + this.id
          this.$http.jsonp(apiUrl_local,
              {
                  jsonp:'_cb_mine'
              }
              )
              .then(function(response) {
                  //console.log(response)
                  this.mapData = response.data.allData
                  this.currentPage = 1
                  this.pageSize = 7
                  console.log("para detail not fucked")
                  console.log(this.tableData)
              }, function(response) {
                  console.log("my site para detail JSON fucked")
              })
      },
      getCustomers_mapdata: function() {
          var apiUrl_local = this.apiUrl_mapdata + this.id
          this.$http.jsonp(apiUrl_local,
              {
                  jsonp:'_cb_mine'
              }
              )
              .then(function(response) {
                  (this.chart.series)[0].data = response.data.allData
                  this.currentPage = 1
                  this.pageSize = 7
                  console.log("para detail not fucked")
                  console.log(this.tableData)
              }, function(response) {
                  console.log("my site para detail JSON fucked")
              })
      },
	    getCustomersFilter: function() {
	        var _msg=JSON.parse(sessionStorage.getItem('_obj'))
	        var apiUrl_local = this.apiUrl_filter + this.id + "&value="+this.value
	        this.$http.jsonp(apiUrl_local,
	            {
	                jsonp:'_cb_mine'
	            }
	            )
	            .then(function(response) {
                  this.allData = response.data.allData
                  this.tableData=this.allData.slice(0,7)
                  this.total=this.allData.length
                  this.currentPage = 1
                  this.pageSize = 7
	                console.log("para detail filtering   not fucked")
	                console.log(this.tableData)
	            }, function(response) {
	                console.log("my site para detail  filtering   JSON fucked")
	            })
	    },
      handleCurrentChange(val) {
        this.currentPage = val;
        var endCount=val*this.pageSize
        var startCount=this.pageSize*(val-1)
        this.tableData=this.allData.slice(startCount,endCount)
      }
    },
    created:function(){
      var _this=this
        setTimeout(function(){
           _this.id=_this.$store.state.login.info.id
            _this.getCustomers_top5()
            _this.getCustomers_mapdata()
            _this.getCustomers()
        },30)
    }


  }
</script>
