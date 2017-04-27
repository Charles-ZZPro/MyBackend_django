#-*-coding:utf-8-*-
from __future__ import unicode_literals
import gzip 
import tarfile
import os
from django.db import models
import psycopg2
import sys
import datetime
import random
import shutil
import socket

#from pyinotify import WatchManager, Notifier, ProcessEvent, IN_DELETE, IN_CREATE, IN_MODIFY

reload(sys)
sys.setdefaultencoding('utf-8')

# class EventHandler(ProcessEvent):
#     def process_IN_CREATE(self, event):
#         print "Create file:%s." %os.path.join(event.path,event.name)

#         os.system('cp -rf %s /tmp/bak/'%(os.path.join(event.path,event.name)))
#     def process_IN_DELETE(self, event):
#         print "Delete file:%s." %os.path.join(event.path,event.name)

#     def process_IN_MODIFY(self, event):
#         print "Modify file:%s." %os.path.join(event.path,event.name)

# def FsMonitor(path='.'):
#     wm = WatchManager()
#     mask = IN_DELETE | IN_CREATE | IN_MODIFY
#     notifier = Notifier(wm, EventHandler())
#     wm.add_watch(path, mask, auto_add= True, rec=True)
#     print "now starting monitor %s." %path

#     while True:
#         try:
#             notifier.process_events()
#             if notifier.check_events():
#                 print "check event true."
#                 notifier.read_events()
#         except KeyboardInterrupt:
#             print "keyboard Interrupt."
#             notifier.stop()
#             break
# def test_moniter:
#     FsMonitor("/home/charles/log/")

# Create your models here.
def get_pgconn():
    # Connect to an existing database
    #conn = psycopg2.connect("dbname=myTestDB user=postgres password=postgres")
    conn = psycopg2.connect("dbname=myTestDB user=littleAdmin password=postgres")
    # Open a cursor to perform database operations
    cur = conn.cursor()
    return cur,conn

def close_pgconn(cur,conn):
    cur.close()    
    conn.close()

def commit_conn(conn):
	conn.commit()

def get_active_totalnums():
    cur,conn= get_pgconn()
    sql_get_act = "select proj_name, proj_id, sum(act_num) cnt_num from table_activate_num_fake group by proj_id, proj_name order by proj_id limit 1"
    cur.execute(sql_get_act)
    results = cur.fetchall()
    close_pgconn(cur,conn)
    result_item = []
    result_str = ""
    
    for item in results:
    	each_result = {}
    	each_result['title'] = item[0]
    	each_result['title'] = each_result['title'].encode('utf-8')
    	#print type(each_result['title'])    	
    	#print each_result['title']
    	each_result['number'] = str(item[2])
        #result_str_each = each_result['title'] + "," + each_result['number']
        result_item.append(each_result)
        result_str = result_str+'{"title":"' + each_result['title'] +'",'+'"number":"' + each_result['number'] + '","id":"'+str(item[1])+'"},'
    #print result_item
    #return HttpResponse("<p>"+str(result_item)+"</p>")
    result_str = result_str[0:int(len(result_str))-1]    
    result_str = '{"tuple":[' + result_str +']}'
    #print result_str
    #result_str = result_str.replace("\","")
    #print result_str
    json_total = {}
    json_total['tuple'] = result_item

    #return json_total
    return result_str

def get_active_dailynums(proj_id):
    # cur,conn = get_pgconn()
    # sql_get_act = "select proj_name,date_s,act_num from table_activate_num where proj_id=" + str(proj_id)+" order by date_s desc"
    # cur.execute(sql_get_act)
    # results = cur.fetchall()
    # close_pgconn(cur,conn)    
    # result_item = []
    # result_str = ""


    cur,conn= get_pgconn()
    sql_get_act = "select date_s,sum(act_num),avg(rate) from table_activate_num_fake where proj_id=" + str(proj_id)+" group by date_s order by date_s desc"
    cur.execute(sql_get_act)
    results = cur.fetchall()
    close_pgconn(cur,conn)

    cur,conn= get_pgconn()
    sql_get_act = "select sum(act_num) from table_activate_num_fake where proj_id=" + str(proj_id)
    cur.execute(sql_get_act)
    results_all = cur.fetchall()
    close_pgconn(cur,conn)

    # cur,conn= get_pgconn()
    # sql_get_act = "select sum(act_num) from table_activate_num_fake"
    # cur.execute(sql_get_act)
    # results_all = cur.fetchall()
    # close_pgconn(cur,conn)

    result_item = []
    result_str = ""
    join_user = ""

    add_num = results_all[0][0]+results[0][1]

    for index ,item in enumerate(results):
        each_result = {}
        each_result['date'] = item[0].encode('utf-8')
        each_result['act_num'] = item[1]
        #each_result['rate'] = '%.4f' %(item[2])
        each_result['rate'] = item[2]
        if index==0:
            add_num = add_num - results[0][1]
        else:
            add_num = add_num-results[index-1][1]

        each_result['lively_num'] = int(add_num*each_result['rate'])
        result_str = result_str+'{date:"' + each_result['date'] +'",'+'activated_num:' + str(each_result['act_num']) + ',addup_num:' + str(add_num) + ',lively_num:' + str(each_result['lively_num']) +'},'
    
    # for item in results:
    # 	each_result = {}
    # 	each_result['date'] = item[1]
    # 	each_result['date'] = each_result['date'].encode('utf-8')
    # 	#print each_result['title']
    # 	#print type(each_result['title'])    	
    # 	each_result['number'] = int(item[2])	
    #     #result_str_each = each_result['title'] + "," + each_result['number']
    #     result_item.append(each_result)

    #     cur,conn = get_pgconn()
    #     sql_get_act_each_total = "select sum(act_num) from table_activate_num where proj_id=" + str(proj_id)+" and date_s<='" + each_result['date'] +"'"
    #     cur.execute(sql_get_act_each_total)
    #     results = cur.fetchall()       
    #     close_pgconn(cur,conn)        

    #     result_str = result_str+'{"date":"' + each_result['date'] +'",'+'"activated_num":"' + str(each_result['number']) + '","addup_num":"' + str(results[0][0]) +'"},'

    result_str = result_str[0:int(len(result_str))-1]    
    result_str = '{"allData":[' + result_str +']}'        
    #print result_item
    #return HttpResponse("<p>"+str(result_item)+"</p>")
    return result_str    

def get_active_dailynums_filter(proj_id,date_range):
    
    print date_range

    date_range_array = date_range.split(",")
    date_range_box = []
    date_from = ""
    date_to = ""

    for j in date_range_array:
        date_array = j.split(' ')
        month = date_array[1]
        day = date_array[2]
        year = date_array[3]
        if month == 'Jan':
            month = '1'
        elif month == 'Feb':
            month = '2' 
        elif month == 'Mar':
            month = '3' 
        elif month == 'Apr':
            month = '4'             
        elif month == 'May':
            month = '5'     
        elif month == 'Jun':
            month = '6' 
        elif month == 'Jul':
            month = '7' 
        elif month == 'Aug':
            month = '8'             
        elif month == 'Sep':
            month = '9'   
        elif month == 'Oct':
            month = '10' 
        elif month == 'Nov':
            month = '11'             
        elif month == 'Dec':
            month = '12' 
        formatted_date = year +"-"+ month +"-"+ day
        date_range_box.append(formatted_date)

    date_from = date_range_box[0]
    date_to = date_range_box[1]

    cur,conn = get_pgconn()
    sql_get_act = "select date_s,sum(act_num),avg(rate) from table_activate_num_fake where proj_id=" + str(proj_id)+" and date_s>='"+date_from+"' and date_s<='" +date_to+"' group by date_s order by date_s desc"
    #sql_get_act = "select proj_name,date_s,act_num from table_activate_num where proj_id=" + str(proj_id)+" and date_s>='"+date_from+"' and date_s<='" +date_to+ "' order by date_s desc"
    cur.execute(sql_get_act)
    results = cur.fetchall()
    close_pgconn(cur,conn)    
    result_item = []
    result_str = ""
    
    if results!=[]:
        for item in results:
            each_result = {}
            each_result['date'] = item[0]
            each_result['date'] = each_result['date'].encode('utf-8')
            #print each_result['title']
            #print type(each_result['title'])       
            each_result['number'] = int(item[1])   
            each_result['rate'] = item[2] 
            #result_str_each = each_result['title'] + "," + each_result['number']
            result_item.append(each_result)

            cur,conn = get_pgconn()
            sql_get_act_each_total = "select sum(act_num) from table_activate_num_fake where proj_id=" + str(proj_id)+" and date_s<='" + each_result['date'] +"'"
            cur.execute(sql_get_act_each_total)
            results = cur.fetchall()       
            close_pgconn(cur,conn)  
            each_result['lively_num'] = int(results[0][0]*each_result['rate'])      

            result_str = result_str+'{"date":"' + each_result['date'] +'",'+'"activated_num":"' + str(each_result['number']) + '","addup_num":"' + str(results[0][0]) +'"'+ ',"lively_num":"' + str(each_result['lively_num']) + '"},'

    result_str = result_str[0:int(len(result_str))-1]    
    result_str = '{"allData":[' + result_str +']}'        
    #print result_item
    #return HttpResponse("<p>"+str(result_item)+"</p>")
    return result_str  

def insert_daily_fake_data():
    now = datetime.datetime.now()
    rand1 = str(random.randint(1000, 1000000))
    rand2 = str(random.randint(1000, 1000000))
    rand3 = str(random.randint(1000, 1000000))
    rand4 = str(random.randint(1000, 1000000))
    date_str = now.strftime('%Y-%m-%d')  

    cur,conn = get_pgconn()
    # cur.execute("insert into table_activate_num(proj_name,date_s,act_num,proj_id) values(%s,%s,%s,%s)",('第一个项目',date_str,rand1,1))
    # conn.commit()
    # cur.execute("insert into table_activate_num(proj_name,date_s,act_num,proj_id) values(%s,%s,%s,%s)",('第二个项目',date_str,rand2,2))    
    # cur.execute("insert into table_activate_num(proj_name,date_s,act_num,proj_id) values(%s,%s,%s,%s)",('第三个项目',date_str,rand3,3))
    # cur.execute("insert into table_activate_num(proj_name,date_s,act_num,proj_id) values(%s,%s,%s,%s)",('第四个test项目',date_str,rand4,4))        
    sql_insert_act = "insert into table_activate_num(proj_name,date_s,act_num,proj_id) values('第一个项目','"+date_str+"',"+rand1+",1);"+\
    "insert into table_activate_num(proj_name,date_s,act_num,proj_id) values('第二个项目','"+date_str+"',"+rand2+",2);"+\
    "insert into table_activate_num(proj_name,date_s,act_num,proj_id) values('第三个项目','"+date_str+"',"+rand3+",3);"+\
    "insert into table_activate_num(proj_name,date_s,act_num,proj_id) values('第四个test项目','"+date_str+"',"+rand4+",4);"

    #print sql_insert_act                    
    cur.execute(sql_insert_act)
    commit_conn(conn)   
    close_pgconn(cur,conn)
    #results = cur.fetchall()
    print " that is enough"
    return "OK"

def insert_daily_fake_data_fortesting():
    now = datetime.datetime.now()

    #now=datetime.datetime.now()

    delta=datetime.timedelta(days=1)

    t_str = '2016-12-29'

    now_fake = datetime.datetime.strptime(t_str,'%Y-%m-%d')
    rand1 = random.randint(5000,5300)

    t_str_end = '2017-01-08'

    t_str_end_fake = datetime.datetime.strptime(t_str_end,'%Y-%m-%d')

    while now_fake.strftime('%Y-%m-%d') < t_str_end_fake.strftime('%Y-%m-%d'):
        now_fake=now_fake+delta

        date_str = now_fake.strftime('%Y-%m-%d')
        #rand1 = random.randint(30,100)
        
        rand1 = rand1 + random.randint(200, 600)
        rand1_uni = random.uniform(0.88,0.92)
        #rand1 = rand1 + random.randint(20, 30)
        
        #rand3 = str(random.randint(1000, 1000000))
        #rand4 = str(random.randint(1000, 1000000))

        date_str = now_fake.strftime('%Y-%m-%d')  

        # cur,conn = get_pgconn()
        # cur.execute("insert into table_activate_num(proj_name,date_s,act_num,proj_id) values(%s,%s,%s,%s)",('第一个项目',date_str,rand1,1))
        # conn.commit()
        # cur.execute("insert into table_activate_num(proj_name,date_s,act_num,proj_id) values(%s,%s,%s,%s)",('第二个项目',date_str,rand2,2))    
        # cur.execute("insert into table_activate_num(proj_name,date_s,act_num,proj_id) values(%s,%s,%s,%s)",('第三个项目',date_str,rand3,3))
        # cur.execute("insert into table_activate_num(proj_name,date_s,act_num,proj_id) values(%s,%s,%s,%s)",('第四个test项目',date_str,rand4,4))        
        sql_insert_act = "insert into table_activate_num_fake(proj_name,date_s,act_num,proj_id,country,rate) values('project_1','"+date_str+"',"+str(rand1)+",1,'China',"+str(rand1_uni)+");"

        #print sql_insert_act                    
        # cur.execute(sql_insert_act)
        # commit_conn(conn)   
        # close_pgconn(cur,conn)
        print sql_insert_act

    #results = cur.fetchall()
    print " that is enough"
    return "OK"

def insert_daily_fake_data_fortesting_rate():
    now = datetime.datetime.now()

    #now=datetime.datetime.now()

    delta=datetime.timedelta(days=1)

    t_str = '2016-10-21'

    now_fake = datetime.datetime.strptime(t_str,'%Y-%m-%d')
    rand1 = random.randint(200,400)

    #while now_fake.strftime('%Y-%m-%d') < now.strftime('%Y-%m-%d'):
        # now_fake=now_fake+delta

        # date_str = now_fake.strftime('%Y-%m-%d')

        
    
    # rand1 = rand1 + random.randint(20, 30)
    # #rand3 = str(random.randint(1000, 1000000))
    # #rand4 = str(random.randint(1000, 1000000))

    # date_str = now_fake.strftime('%Y-%m-%d')  


    # cur.execute("insert into table_activate_num(proj_name,date_s,act_num,proj_id) values(%s,%s,%s,%s)",('第一个项目',date_str,rand1,1))
    # conn.commit()
    # cur.execute("insert into table_activate_num(proj_name,date_s,act_num,proj_id) values(%s,%s,%s,%s)",('第二个项目',date_str,rand2,2))    
    # cur.execute("insert into table_activate_num(proj_name,date_s,act_num,proj_id) values(%s,%s,%s,%s)",('第三个项目',date_str,rand3,3))
    # cur.execute("insert into table_activate_num(proj_name,date_s,act_num,proj_id) values(%s,%s,%s,%s)",('第四个test项目',date_str,rand4,4)) 
    for id_got in range(1105,2500): 
        cur,conn = get_pgconn()        
        rand1 = random.uniform(0.20,0.99)      
        #sql_insert_act = "update table_activate_num_fake set rate="+str(rand1)+" where country='bra' and id="+str(id_got)
        sql_insert_act = "update table_activate_num_fake set rate="+str(rand1)+" where id="+str(id_got)
        print sql_insert_act
        id_got=id_got+1
        cur.execute(sql_insert_act)
        commit_conn(conn)   
        close_pgconn(cur,conn)        

    #print sql_insert_act                    


    #results = cur.fetchall()
    print " that is enough"
    return "OK"

def insert_daily_fake_data_fortesting_daily():
    now = datetime.datetime.now()

    #now=datetime.datetime.now()

    #delta=datetime.timedelta(days=1)

    #$t_str = '2016-10-21'

    #now_fake = datetime.datetime.strptime(t_str,'%Y-%m-%d')
    rand1 = random.randint(200,400)

    #while now_fake.strftime('%Y-%m-%d') < now.strftime('%Y-%m-%d'):
        # now_fake=now_fake+delta

        # date_str = now_fake.strftime('%Y-%m-%d')

        
    
    # rand1 = rand1 + random.randint(20, 30)
    # #rand3 = str(random.randint(1000, 1000000))
    # #rand4 = str(random.randint(1000, 1000000))

    # date_str = now_fake.strftime('%Y-%m-%d')  
    date_str = now.strftime('%Y-%m-%d')  

    # cur.execute("insert into table_activate_num(proj_name,date_s,act_num,proj_id) values(%s,%s,%s,%s)",('第一个项目',date_str,rand1,1))
    # conn.commit()
    # cur.execute("insert into table_activate_num(proj_name,date_s,act_num,proj_id) values(%s,%s,%s,%s)",('第二个项目',date_str,rand2,2))    
    # cur.execute("insert into table_activate_num(proj_name,date_s,act_num,proj_id) values(%s,%s,%s,%s)",('第三个项目',date_str,rand3,3))
    # cur.execute("insert into table_activate_num(proj_name,date_s,act_num,proj_id) values(%s,%s,%s,%s)",('第四个test项目',date_str,rand4,4)) 


    # for id_got in range(71,1000): 
    #     cur,conn = get_pgconn()        
    #     rand1 = random.uniform(0.87,0.93)      
    #     sql_insert_act = "insert into table_activate_num_fake(proj_name,date_s,act_num,proj_id,country) values('project_1','"+date_str+"',"+str(rand1)+",1,'us');"
    #     print sql_insert_act
    #     id_got=id_got+1
    #     cur.execute(sql_insert_act)
    #     commit_conn(conn)   
    #     close_pgconn(cur,conn)        


    #print sql_insert_act                    


    #results = cur.fetchall()
    print " that is enough"
    return "OK"

def get_list_by_date():
    cur,conn= get_pgconn()
    sql_get_act = "select date_s,sum(act_num),avg(rate) from table_activate_num_fake group by date_s order by date_s desc"
    cur.execute(sql_get_act)
    results = cur.fetchall()
    close_pgconn(cur,conn)

    cur,conn= get_pgconn()
    sql_get_act = "select sum(act_num) from table_activate_num_fake"
    cur.execute(sql_get_act)
    results_all = cur.fetchall()
    close_pgconn(cur,conn)

    result_item = []
    result_str = ""
    join_user = ""

    add_num = results_all[0][0]+results[0][1]

    for index ,item in enumerate(results):
        each_result = {}
        each_result['date'] = item[0].encode('utf-8')
        each_result['act_num'] = item[1]
        #each_result['rate'] = '%.4f' %(item[2])
        each_result['rate'] = item[2]
        if index==0:
            add_num = add_num - results[0][1]
        else:
            add_num = add_num-results[index-1][1]

        each_result['lively_num'] = int(add_num*each_result['rate'])
        result_str = result_str+'{date:"' + each_result['date'] +'",'+'activated_num:' + str(each_result['act_num']) + ',addup_num:' + str(add_num) + ',lively_num:' + str(each_result['lively_num']) +'},'
   
    #result_str = join_user 
    result_str = result_str[0:int(len(result_str))-1]  
    result_str = '{tuple:[' + result_str +']}'   

    #print result_str
    return result_str

def get_list_by_country():
    cur,conn= get_pgconn()
    sql_get_act = "select country,sum(act_num) s,avg(rate) from table_activate_num_fake group by country order by s desc"
    cur.execute(sql_get_act)
    results = cur.fetchall()
    close_pgconn(cur,conn)
    result_item = []
    result_str = ""
    join_user = ""

    add_num = 2645225+75170

    for index ,item in enumerate(results):
        each_result = {}        

        each_result['country'] = item[0]
        if each_result['country']=='india':
            each_result['country'] = '印度'
        elif each_result['country']=='indonisia':
            each_result['country'] = '印度尼西亚'
        elif each_result['country']=='viet':      
             each_result['country'] = '越南'
        elif each_result['country']=='spain':
            each_result['country'] = '西班牙'
        elif each_result['country']=='italy':  
            each_result['country'] = '意大利'
        elif each_result['country']=='malay':
            each_result['country'] = '马来西亚'
        elif each_result['country']=='bra':  
            each_result['country'] = '巴西'
        elif each_result['country']=='eng':
            each_result['country'] = '英国'
        elif each_result['country']=='taiwan': 
             each_result['country'] = '台湾'
        elif each_result['country']=='us':
            each_result['country'] = '美国'
        elif each_result['country']=='cn':  
            each_result['country'] = '中国'
        elif each_result['country']=='thai':
            each_result['country'] = '泰国'

        each_result['country'] = each_result['country'].encode('utf-8')
        each_result['act_num'] = item[1]
        each_result['rate'] = item[2]
        if index==0:
            add_num = add_num - 75170
        else:
            add_num = add_num-results[index-1][1]
        rate_country = str('%.2f'%((each_result['act_num']/2645225.0)*100.0))+"%"

        each_result['lively_num'] = int(add_num*each_result['rate'])
        result_str = result_str+'{name:"' + each_result['country'] +'",'+'value:' + str(each_result['act_num'])+',percent:"'+str(rate_country)+'"},'
   
    result_str = result_str[0:int(len(result_str))-1]  
    result_str = '{tuple:[' + result_str +']}'   

    #print result_str
    return result_str

def get_user_info():
    cur,conn= get_pgconn()
    sql_get_act = "select user_name, passwd ,status from table_user"
    cur.execute(sql_get_act)
    results = cur.fetchall()
    close_pgconn(cur,conn)
    result_item = []
    result_str = ""
    join_user = ""

    for item in results:
        each_result = {}
        each_result['user_name'] = item[0].encode('utf-8')
        each_result['passwd'] = item[1].encode('utf-8')
        each_result['status'] = item[2].encode('utf-8')
        join_user = join_user + each_result['user_name'] + each_result['passwd'] +each_result['status']+ "Mypassinstringhere"
 
    result_str = join_user 
    result_str = '{"tuple":"' + result_str +'"}'
    print result_str

    return result_str

def get_top5_lively_country(proj_id):
    print "wocacca"
    cur,conn= get_pgconn()
    sql_get_all = "select sum(act_num) from table_activate_num_fake  where proj_id=" + str(proj_id)
    cur.execute(sql_get_all)
    results_all = cur.fetchall()
    close_pgconn(cur,conn)

    count_all = results_all[0][0]

    cur,conn= get_pgconn()
    sql_get_top5 = "select country,sum(act_num) sum from table_activate_num_fake where proj_id=" + str(proj_id)+" group by country order by sum desc limit 5 "
    cur.execute(sql_get_top5)
    results_top5 = cur.fetchall()
    close_pgconn(cur,conn)

    result_str = ""

    for item in results_top5:
        each_result = {}
        each_result['country'] = item[0].encode('utf-8')
        each_result['sum'] = item[1]

        each_result['rate'] = str('%.2f'%((float(each_result['sum'])/count_all)*100.0))+"%"
        result_str = result_str + '{name:"' + each_result['country'] +'",'+'value:' + str(each_result['sum'])+',percent:"'+str(each_result['rate'])+'"},'
 
    result_str = result_str[0:int(len(result_str))-1]  
    result_str = '{allData:[' + result_str +']}'   
    print result_str

    return result_str    

def get_map_data(proj_id):
    cur,conn= get_pgconn()
    sql_get_all = "select sum(act_num) from table_activate_num_fake where proj_id=" + str(proj_id)
    cur.execute(sql_get_all)
    results_all = cur.fetchall()
    close_pgconn(cur,conn)

    count_all = results_all[0][0]

    cur,conn= get_pgconn()
    sql_get_top5 = "select country,sum(act_num) sum from table_activate_num_fake where proj_id=" + str(proj_id) +" group by country order by sum desc"
    cur.execute(sql_get_top5)
    results_top5 = cur.fetchall()
    close_pgconn(cur,conn)

    result_str = ""

    for item in results_top5:
        each_result = {}
        each_result['country'] = item[0].encode('utf-8')
        each_result['sum'] = item[1]

        each_result['rate'] = str('%.2f'%((float(each_result['sum'])/count_all)*100.0))+"%"
        result_str = result_str + '{name:"' + each_result['country'] +'",'+'value:' + str(each_result['sum'])+',percent:"'+str(each_result['rate'])+'"},'
 
    result_str = result_str[0:int(len(result_str))-1]  
    result_str = '{allData:[' + result_str +']}'
    print result_str

    return result_str

def putting_data():
    cur,conn = get_pgconn()        
    #rand1 = random.uniform(0.20,0.99)      
    #sql_insert_act = "update table_activate_num_fake set rate="+str(rand1)+" where country='bra' and id="+str(id_got)
    sql_insert_act = "update table_activate_num_fake set proj_id=1 where date_s>'2017-01-05'"
    #print sql_insert_act
    #id_got=id_got+1
    cur.execute(sql_insert_act)
    commit_conn(conn)   
    close_pgconn(cur,conn)     

    return "OK"

# def insert_formatted_data_to_db_daily()

#     #now = datetime.datetime.now()    
#     #file_name = '/home/charles/log/production_2016-11-28.log.tar.gz'

#     #t = tarfile.open(fname)
#     #t.extractall(path = ".")
#     #log_file_name = '/home/charles/log/production_2016-11-28.log.3'

#     file_name = '/home/charles/log/'+file_name

#     """ungz zip file"""  
#     f_name_tar = file_name.replace(".gz", "")  
#     #获取文件的名称，去掉  
#     g_file = gzip.GzipFile(file_name)  
#     #创建gzip对象  
#     open(f_name_tar, "w+").write(g_file.read())  
#     #gzip对象用read()打开后，写入open()建立的文件中。  
#     g_file.close()  
#     #关闭gzip对象


#     """untar zip file"""  
#     tar = tarfile.open(f_name_tar)  
#     names = tar.getnames()  
#     if os.path.isdir(f_name_tar + "_files"):  
#         pass  
#     else:  
#         os.mkdir(f_name_tar + "_files")  
#     #由于解压后是许多文件，预先建立同名文件夹  
#     for name in names:  
#         tar.extract(name, f_name_tar + "_files/")  
#     tar.close()  

#     for file in os.listdir(f_name_tar + "_files/"):
#         f = open(f_name_tar + "_files/"+file)
#         #f = open(file)
#         for i in f:
#             if i.count('android_id')==0:
#                 continue
#             else:
#                 ind_imsi = i.index('imsi')
#                 ind_imei = i.index('imei')
#                 ind_androidid = i.index('android_id')
#                 ind_mac = i.index('wifi_mac')

#                 imsi = i[ind_imsi+7:ind_imsi+22]
#                 imei = i[ind_imei+7:ind_imei+22]
#                 android_id = i[ind_androidid+13:ind_androidid+28]
#                 wifi_mac = i[ind_mac+11:ind_mac+28]

#                 info_join = imsi+"$&&&#####"+imei+"$&&&#####"+android_id+"$&&&#####"+wifi_mac

#                 cur,conn= get_pgconn()
#                 sql_get_all = "select count(id) from table_activate_num_ids  where imsi='" + imsi + "' or imei='" + imei +"' or android_id='"+android_id+"' or wifi_mac='"+wifi_mac+"'"
#                 cur.execute(sql_get_all)
#                 results_all = cur.fetchall()
#                 close_pgconn(cur,conn)

#                 if results_all[0][0]==0:
#                     cur,conn = get_pgconn()  
#                     sql_insert_act = "insert into table_activate_num_ids(imsi,imei,android_id,wifi_mac,date_s) values('"+ imsi + "','" + imei + "','" + android_id + "','" + wifi_mac +"','"+time+"')"             
#                     cur.execute(sql_insert_act)
#                     commit_conn(conn)   
#                     close_pgconn(cur,conn)         

#                 if imsi.count("UNKNOWN")>0 or imei.count("UNKNOWN")>0:
#                     cur,conn= get_pgconn()
#                     sql_get_all_unk = "select count(id) from table_activate_num_ids  where android_id='"+android_id+"' or wifi_mac='"+wifi_mac+"'"
#                     cur.execute(sql_get_all_unk)
#                     results_all_unk = cur.fetchall()
#                     close_pgconn(cur,conn)   

#                     if results_all_unk[0][0]==0: 
#                         cur,conn = get_pgconn()  
#                         sql_insert_act = "insert into table_activate_num_ids(imsi,imei,android_id,wifi_mac,date_s) values('"+ imsi + "','" + imei + "','" + android_id + "','" + wifi_mac +"','"+time+"')"             
#                         cur.execute(sql_insert_act)
#                         commit_conn(conn)   
#                         close_pgconn(cur,conn)            

#     #os.remove(file_name)
#     os.remove(f_name_tar)
#     shutil.rmtree(f_name_tar + "_files/")

#     return "OK"

#create table for daily active
def create_new_table_for_daily_active():

    now_t = datetime.datetime.now()
    now_str_t = now_t.strftime('%Y_%m_%d')
    daily_table = "table_daily_active_"+now_str_t

    cur,conn = get_pgconn()  
    sql_create_seq = 'CREATE SEQUENCE public.'+daily_table+'_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 99999999 START 1 CACHE 1;'+'ALTER TABLE public.'+daily_table+'_id_seq OWNER TO "littleAdmin";'    
    cur.execute(sql_create_seq)
    commit_conn(conn)   
    close_pgconn(cur,conn) 

    cur,conn = get_pgconn() 
    sql_create= 'CREATE TABLE public.'+daily_table+"(id integer NOT NULL DEFAULT nextval('"+daily_table+"_id_seq'::regclass),"+'imsi text,'\
      'imei text,'\
      'android_id text,'\
      'wifi_mac text,'\
      'date_s text,'\
      'proj_name text,'\
      'sub_channel_name text,'\
      'sub_channel_id text,'\
      'CONSTRAINT '+daily_table+'_pkey PRIMARY KEY (id))'\
      'WITH (OIDS=FALSE);'\
      'ALTER TABLE public.'+daily_table+' OWNER TO "littleAdmin";'
    cur.execute(sql_create)
    commit_conn(conn)   
    close_pgconn(cur,conn) 

    return "OK"

#create table for daily active(2016 passed)
def create_new_table_for_daily_active_pass(date):

    # now_t = datetime.datetime.now()
    # now_str_t = now_t.strftime('%Y_%m_%d')
    # daily_table = "table_daily_active_"+now_str_t
    daily_table = "table_daily_active_"+date

    cur,conn = get_pgconn()  
    sql_create_seq = 'CREATE SEQUENCE public.'+daily_table+'_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 99999999 START 1 CACHE 1;'+'ALTER TABLE public.'+daily_table+'_id_seq OWNER TO "littleAdmin";'    
    cur.execute(sql_create_seq)
    commit_conn(conn)   
    close_pgconn(cur,conn) 

    cur,conn = get_pgconn() 
    sql_create= 'CREATE TABLE public.'+daily_table+"(id integer NOT NULL DEFAULT nextval('"+daily_table+"_id_seq'::regclass),"+'imsi text,'\
      'imei text,'\
      'android_id text,'\
      'wifi_mac text,'\
      'date_s text,'\
      'proj_name text,'\
      'sub_channel_name text,'\
      'sub_channel_id text,'\
      'CONSTRAINT '+daily_table+'_pkey PRIMARY KEY (id))'\
      'WITH (OIDS=FALSE);'\
      'ALTER TABLE public.'+daily_table+' OWNER TO "littleAdmin";'      
    cur.execute(sql_create)
    commit_conn(conn)   
    close_pgconn(cur,conn) 

    return "OK"


#从rawdata压缩文件中提取有效新增独立用户，插入数据库
def insert_formatted_data_to_db(file_name,time,proj_name):

    time = time[0:10]

    #now = datetime.datetime.now()    
    #file_name = '/home/charles/log/production_2016-11-28.log.tar.gz'

    #t = tarfile.open(fname)
    #t.extractall(path = ".")
    #log_file_name = '/home/charles/log/production_2016-11-28.log.3'

    file_name = '/home/charles/log/'+file_name

    """ungz zip file"""  
    f_name_tar = file_name.replace(".gz", "")  
    #获取文件的名称，去掉  
    g_file = gzip.GzipFile(file_name)  
    #创建gzip对象  
    open(f_name_tar, "w+").write(g_file.read())  
    #gzip对象用read()打开后，写入open()建立的文件中。  
    g_file.close()  
    #关闭gzip对象


    """untar zip file"""  
    tar = tarfile.open(f_name_tar)  
    names = tar.getnames()  
    if os.path.isdir(f_name_tar + "_files"):  
        pass  
    else:  
        os.mkdir(f_name_tar + "_files")  
    #由于解压后是许多文件，预先建立同名文件夹  
    for name in names:  
        tar.extract(name, f_name_tar + "_files/")  
    tar.close()  

    for file in os.listdir(f_name_tar + "_files/"):
        f = open(f_name_tar + "_files/"+file)
        #f = open(file)
        for i in f:
            if i.count('android_id')==0:
                continue
            else:
                ind_imsi = i.index('imsi')
                ind_imei = i.index('imei')
                ind_androidid = i.index('android_id')
                ind_mac = i.index('wifi_mac')

                imsi = i[ind_imsi+7:ind_imsi+22]
                imei = i[ind_imei+7:ind_imei+22]
                android_id = i[ind_androidid+13:ind_androidid+28]
                wifi_mac = i[ind_mac+11:ind_mac+28]

                #info_join = imsi+"$&&&#####"+imei+"$&&&#####"+android_id+"$&&&#####"+wifi_mac

                ### calculating independent users
                cur,conn= get_pgconn()
                #sql_get_all = "select count(id) from table_activate_num_ids  where imsi='" + imsi + "' or imei='" + imei +"' or android_id='"+android_id+"' or wifi_mac='"+wifi_mac+"' and proj_name='"+proj_name+"'"
                sql_get_all = "select count(id) from table_activate_num_ids  where imsi='" + imsi + "' or android_id='"+android_id+"' or wifi_mac='"+wifi_mac+"' and proj_name='"+proj_name+"'"
                cur.execute(sql_get_all)
                results_all = cur.fetchall()
                close_pgconn(cur,conn)

                if results_all[0][0]==0:
                    cur,conn = get_pgconn()  
                    sql_insert_act = "insert into table_activate_num_ids(imsi,imei,android_id,wifi_mac,date_s,proj_name) values('"+ imsi + "','" + imei + "','" + android_id + "','" + wifi_mac +"','"+time+"','"+proj_name+"')"             
                    cur.execute(sql_insert_act)
                    commit_conn(conn)   
                    close_pgconn(cur,conn)         

                if imsi.count("UNKNOWN")>0 or imei.count("UNKNOWN")>0:
                    cur,conn= get_pgconn()
                    sql_get_all_unk = "select count(id) from table_activate_num_ids  where android_id='"+android_id+"' or wifi_mac='"+wifi_mac+"' and proj_name='"+proj_name+"'"
                    cur.execute(sql_get_all_unk)
                    results_all_unk = cur.fetchall()
                    close_pgconn(cur,conn)   

                    if results_all_unk[0][0]==0: 
                        cur,conn = get_pgconn()  
                        sql_insert_act = "insert into table_activate_num_ids(imsi,imei,android_id,wifi_mac,date_s,proj_name) values('"+ imsi + "','" + imei + "','" + android_id + "','" + wifi_mac +"','"+time+"','"+proj_name+"')"             
                        cur.execute(sql_insert_act)
                        commit_conn(conn)   
                        close_pgconn(cur,conn) 

                ### calculating daily active users
                now_t = datetime.datetime.now()
                now_str_t = now_t.strftime('%Y_%m_%d')
                daily_table = "table_daily_active_"+now_str_t

                cur,conn= get_pgconn()
                #sql_get_all = "select count(id) from "+daily_table+"  where imsi='" + imsi + "' or imei='" + imei +"' or android_id='"+android_id+"' or wifi_mac='"+wifi_mac+"' and proj_name='"+proj_name+"'"
                sql_get_all = "select count(id) from "+daily_table+"  where imsi='" + imsi + "' or android_id='"+android_id+"' or wifi_mac='"+wifi_mac+"' and proj_name='"+proj_name+"'"
                cur.execute(sql_get_all)
                results_all = cur.fetchall()
                close_pgconn(cur,conn)

                if results_all[0][0]==0:
                    cur,conn = get_pgconn()  
                    sql_insert_act = "insert into "+daily_table+"(imsi,imei,android_id,wifi_mac,date_s,proj_name) values('"+ imsi + "','" + imei + "','" + android_id + "','" + wifi_mac +"','"+time+"','"+proj_name+"')"             
                    cur.execute(sql_insert_act)
                    commit_conn(conn)   
                    close_pgconn(cur,conn)         

                if imsi.count("UNKNOWN")>0 or imei.count("UNKNOWN")>0:
                    cur,conn= get_pgconn()
                    sql_get_all_unk = "select count(id) from "+daily_table+"  where android_id='"+android_id+"' or wifi_mac='"+wifi_mac+"' and proj_name='"+proj_name+"'"
                    cur.execute(sql_get_all_unk)
                    results_all_unk = cur.fetchall()
                    close_pgconn(cur,conn)   

                    if results_all_unk[0][0]==0: 
                        cur,conn = get_pgconn()  
                        sql_insert_act = "insert into "+daily_table+"(imsi,imei,android_id,wifi_mac,date_s,proj_name) values('"+ imsi + "','" + imei + "','" + android_id + "','" + wifi_mac +"','"+time+"','"+proj_name+"')"             
                        cur.execute(sql_insert_act)
                        commit_conn(conn)   
                        close_pgconn(cur,conn)            

    #os.remove(file_name)
    # os.remove(f_name_tar)
    shutil.rmtree(f_name_tar + "_files/")

    return "OK"

#从rawdata压缩文件中提取有效新增独立用户，插入数据库
def insert_formatted_data_to_db_pass(file_name,time,proj_name):

    time = time[0:10]

    #now = datetime.datetime.now()    
    #file_name = '/home/charles/log/production_2016-11-28.log.tar.gz'

    #t = tarfile.open(fname)
    #t.extractall(path = ".")
    #log_file_name = '/home/charles/log/production_2016-11-28.log.3'

    file_name = '/home/charles/log/'+file_name

    """ungz zip file"""  
    f_name_tar = file_name.replace(".gz", "")  
    #获取文件的名称，去掉  
    g_file = gzip.GzipFile(file_name)  
    #创建gzip对象  
    open(f_name_tar, "w+").write(g_file.read())  
    #gzip对象用read()打开后，写入open()建立的文件中。  
    g_file.close()  
    #关闭gzip对象


    """untar zip file"""  
    tar = tarfile.open(f_name_tar)  
    names = tar.getnames()  
    if os.path.isdir(f_name_tar + "_files"):  
        pass  
    else:  
        os.mkdir(f_name_tar + "_files")  
    #由于解压后是许多文件，预先建立同名文件夹  
    ############ 2016 passed start
    print "extracting begin !!!!!!!!!!!!!!!!!!!!!!!!!!!!!1"
    ############ 2016 passed end     
    for name in names:  
        tar.extract(name, f_name_tar + "_files/")  
    tar.close()  
    ############ 2016 passed start
    print "extracting over !!!!!!!!!!!!!!!!!!!!!!!!!!!!!1"
    ############ 2016 passed end  
    ############ 2016 passed start
    time = ""
    time_p = ""
    daily_table_last = ""
    daily_table_list = []
    ############ 2016 passed end 
    for file in os.listdir(f_name_tar + "_files/"):
        f = open(f_name_tar + "_files/"+file)
        ############ 2016 passed start
        print file
        ############ 2016 passed end       

        #f = open(file)

        for i in f: 
            if i.count('android_id')==0:
                ############ 2016 passed start
                if i.count(']  INFO -- : [')!=0:
                    time = i[4:14]
                    time_p = time.replace("-","_")
                ############ 2016 passed end                
                continue
            else:
                ind_imsi = i.index('imsi')
                ind_imei = i.index('imei')
                ind_androidid = i.index('android_id')
                ind_mac = i.index('wifi_mac')

                imsi = i[ind_imsi+7:ind_imsi+22]
                imei = i[ind_imei+7:ind_imei+22]
                android_id = i[ind_androidid+13:ind_androidid+28]
                wifi_mac = i[ind_mac+11:ind_mac+28]

                #info_join = imsi+"$&&&#####"+imei+"$&&&#####"+android_id+"$&&&#####"+wifi_mac

                ### calculating independent users
                cur,conn= get_pgconn()
                #sql_get_all = "select count(id) from table_activate_num_ids  where imsi='" + imsi + "' or imei='" + imei +"' or android_id='"+android_id+"' or wifi_mac='"+wifi_mac+"' and proj_name='"+proj_name+"'"
                sql_get_all = "select count(id) from table_activate_num_ids  where imsi='" + imsi + "' or android_id='"+android_id+"' or wifi_mac='"+wifi_mac+"' and proj_name='"+proj_name+"'"
                cur.execute(sql_get_all)
                results_all = cur.fetchall()
                close_pgconn(cur,conn)

                if results_all[0][0]==0:
                    cur,conn = get_pgconn()  
                    sql_insert_act = "insert into table_activate_num_ids(imsi,imei,android_id,wifi_mac,date_s,proj_name) values('"+ imsi + "','" + imei + "','" + android_id + "','" + wifi_mac +"','"+time+"','"+proj_name+"')"             
                    cur.execute(sql_insert_act)
                    commit_conn(conn)   
                    close_pgconn(cur,conn)         

                if imsi.count("UNKNOWN")>0 or imei.count("UNKNOWN")>0:
                    cur,conn= get_pgconn()
                    sql_get_all_unk = "select count(id) from table_activate_num_ids  where android_id='"+android_id+"' or wifi_mac='"+wifi_mac+"' and proj_name='"+proj_name+"'"
                    cur.execute(sql_get_all_unk)
                    results_all_unk = cur.fetchall()
                    close_pgconn(cur,conn)   

                    if results_all_unk[0][0]==0: 
                        cur,conn = get_pgconn()  
                        sql_insert_act = "insert into table_activate_num_ids(imsi,imei,android_id,wifi_mac,date_s,proj_name) values('"+ imsi + "','" + imei + "','" + android_id + "','" + wifi_mac +"','"+time+"','"+proj_name+"')"             
                        cur.execute(sql_insert_act)
                        commit_conn(conn)   
                        close_pgconn(cur,conn) 

                ### calculating daily active users

                now_t = datetime.datetime.now()
                now_str_t = now_t.strftime('%Y_%m_%d')
                daily_table = "table_daily_active_"+now_str_t
           
                ############ 2016 passed start
                daily_table = "table_daily_active_"+time_p
                #daily_table_last = daily_table     
                if daily_table in daily_table_list:
                    print "daily table existed !!!!!"   
                else:
                    create_new_table_for_daily_active_pass(time_p)
                    daily_table_last = daily_table
                    daily_table_list.append(daily_table)
                ############ 2016 passed end                


                cur,conn= get_pgconn()
                #sql_get_all = "select count(id) from "+daily_table+"  where imsi='" + imsi + "' or imei='" + imei +"' or android_id='"+android_id+"' or wifi_mac='"+wifi_mac+"' and proj_name='"+proj_name+"'"
                sql_get_all = "select count(id) from "+daily_table+"  where imsi='" + imsi + "' or android_id='"+android_id+"' or wifi_mac='"+wifi_mac+"' and proj_name='"+proj_name+"'"
                cur.execute(sql_get_all)
                results_all = cur.fetchall()
                close_pgconn(cur,conn)

                if results_all[0][0]==0:
                    cur,conn = get_pgconn()  
                    sql_insert_act = "insert into "+daily_table+"(imsi,imei,android_id,wifi_mac,date_s,proj_name) values('"+ imsi + "','" + imei + "','" + android_id + "','" + wifi_mac +"','"+time+"','"+proj_name+"')"             
                    cur.execute(sql_insert_act)
                    commit_conn(conn)   
                    close_pgconn(cur,conn)         

                if imsi.count("UNKNOWN")>0 or imei.count("UNKNOWN")>0:
                    cur,conn= get_pgconn()
                    sql_get_all_unk = "select count(id) from "+daily_table+"  where android_id='"+android_id+"' or wifi_mac='"+wifi_mac+"' and proj_name='"+proj_name+"'"
                    cur.execute(sql_get_all_unk)
                    results_all_unk = cur.fetchall()
                    close_pgconn(cur,conn)   

                    if results_all_unk[0][0]==0: 
                        cur,conn = get_pgconn()  
                        sql_insert_act = "insert into "+daily_table+"(imsi,imei,android_id,wifi_mac,date_s,proj_name) values('"+ imsi + "','" + imei + "','" + android_id + "','" + wifi_mac +"','"+time+"','"+proj_name+"')"             
                        cur.execute(sql_insert_act)
                        commit_conn(conn)   
                        close_pgconn(cur,conn)            

    #os.remove(file_name)
    # os.remove(f_name_tar)
    shutil.rmtree(f_name_tar + "_files/")

    print daily_table_list

    return "OK"


def compare(x, y):

    DIR = "/home/charles/log/kkk_files"

    stat_x = os.stat(DIR + "/" + x)

    stat_y = os.stat(DIR + "/" + y)

    if stat_x.st_ctime < stat_y.st_ctime:
        return -1
    elif stat_x.st_ctime > stat_y.st_ctime:
        return 1
    else:
        return 0


#从rawdata压缩文件中提取有效新增独立用户，插入数据库
def insert_formatted_data_to_db_pass_new_2017():

    proj_name = "Tripics"
    # time = time[0:10]

    # #now = datetime.datetime.now()    
    # #file_name = '/home/charles/log/production_2016-11-28.log.tar.gz'

    # #t = tarfile.open(fname)
    # #t.extractall(path = ".")
    # #log_file_name = '/home/charles/log/production_2016-11-28.log.3'

    # file_name = '/home/charles/log/'+file_name

    # """ungz zip file"""  
    # f_name_tar = file_name.replace(".gz", "")  
    # #获取文件的名称，去掉  
    # g_file = gzip.GzipFile(file_name)  
    # #创建gzip对象  
    # open(f_name_tar, "w+").write(g_file.read())  
    # #gzip对象用read()打开后，写入open()建立的文件中。  
    # g_file.close()  
    # #关闭gzip对象


    # """untar zip file"""  
    # tar = tarfile.open(f_name_tar)  
    # names = tar.getnames()  
    # if os.path.isdir(f_name_tar + "_files"):  
    #     pass  
    # else:  
    #     os.mkdir(f_name_tar + "_files")  
    # #由于解压后是许多文件，预先建立同名文件夹  
    # ############ 2016 passed start
    # print "extracting begin !!!!!!!!!!!!!!!!!!!!!!!!!!!!!1"
    # ############ 2016 passed end     
    # for name in names:  
    #     tar.extract(name, f_name_tar + "_files/")  
    # tar.close()  
    # ############ 2016 passed start
    # print "extracting over !!!!!!!!!!!!!!!!!!!!!!!!!!!!!1"
    # ############ 2016 passed end  
    # ############ 2016 passed start
    time = ""
    time_p = ""
    daily_table_last = ""

    sql_get_tables = "select pg_tables.tablename from pg_tables order by pg_tables.tablename where pg_tables.tablename LIKE 'table_daily_active_%'"
    cur,conn= get_pgconn()
    cur.execute(sql_get_tables)
    results_get_tables = cur.fetchall()
    close_pgconn(cur,conn)    

    daily_table_list = []
    for item_tables in results_get_tables:
        daily_table_list.append(item_tables[0])

    f_name_tar = "/home/charles/log/kkk"

    ############ 2016 passed end 

    count_loop = 0

    # iterms = os.listdir(f_name_tar + "_files/")
    # iterms.sort(compare)   
    # for item in iterms:
    #     print str(item)
    # # print iterms
    # return "getting out"

    for file in os.listdir(f_name_tar + "_files/"):
        f = open(f_name_tar + "_files/"+file)
        ############ 2016 passed start
        print ("file_name : "+str(file))
        ############ 2016 passed end       
        if file.count('production_')==0:
            print "Not log file !!!!!"
            # os.remove(f_name_tar + "_files/"+file)
            continue

        now_t = datetime.datetime.now()
        now_str_t = now_t.strftime('%Y-%m-%d')
        
        # log_name = "production_"+now_str_t
        
        # if file.count(log_name)==0:
        #     print "log file too old !!!!! deleting it"
        #     os.remove(f_name_tar + "_files/"+file)
        #     continue

        # if count_loop>=5:
        #     break

        #f = open(file)

        for i in f: 
            if i.count('android_id')!=0:
                ind_imsi = i.index('imsi')
                ind_imei = i.index('imei')
                ind_androidid = i.index('android_id')
                ind_mac = i.index('wifi_mac')

                imsi = i[ind_imsi+7:ind_imsi+22]
                imei = i[ind_imei+7:ind_imei+22]
                android_id = i[ind_androidid+13:ind_androidid+28]
                wifi_mac = i[ind_mac+11:ind_mac+28]

                #info_join = imsi+"$&&&#####"+imei+"$&&&#####"+android_id+"$&&&#####"+wifi_mac

                ### calculating independent users
                cur,conn= get_pgconn()
                #sql_get_all = "select count(id) from table_activate_num_ids  where imsi='" + imsi + "' or imei='" + imei +"' or android_id='"+android_id+"' or wifi_mac='"+wifi_mac+"' and proj_name='"+proj_name+"'"
                sql_get_all = "select count(id) from table_activate_num_ids  where imsi='" + imsi + "' or android_id='"+android_id+"' or wifi_mac='"+wifi_mac+"' and proj_name='"+proj_name+"'"
                cur.execute(sql_get_all)
                results_all = cur.fetchall()
                close_pgconn(cur,conn)

                if results_all[0][0]==0:
                    cur,conn = get_pgconn()  
                    sql_insert_act = "insert into table_activate_num_ids(imsi,imei,android_id,wifi_mac,date_s,proj_name) values('"+ imsi + "','" + imei + "','" + android_id + "','" + wifi_mac +"','"+time+"','"+proj_name+"')"             
                    cur.execute(sql_insert_act)
                    commit_conn(conn)   
                    close_pgconn(cur,conn)         

                if imsi.count("UNKNOWN")>0 or imei.count("UNKNOWN")>0:
                    cur,conn= get_pgconn()
                    sql_get_all_unk = "select count(id) from table_activate_num_ids  where android_id='"+android_id+"' or wifi_mac='"+wifi_mac+"' and proj_name='"+proj_name+"'"
                    cur.execute(sql_get_all_unk)
                    results_all_unk = cur.fetchall()
                    close_pgconn(cur,conn)   

                    if results_all_unk[0][0]==0: 
                        cur,conn = get_pgconn()  
                        sql_insert_act = "insert into table_activate_num_ids(imsi,imei,android_id,wifi_mac,date_s,proj_name) values('"+ imsi + "','" + imei + "','" + android_id + "','" + wifi_mac +"','"+time+"','"+proj_name+"')"             
                        cur.execute(sql_insert_act)
                        commit_conn(conn)   
                        close_pgconn(cur,conn) 

                ### calculating daily active users

                now_t = datetime.datetime.now()
                now_str_t = now_t.strftime('%Y_%m_%d')
                daily_table = "table_daily_active_"+now_str_t
           
                ############ 2016 passed start
                daily_table = "table_daily_active_"+time_p
                #daily_table_last = daily_table     
                if daily_table in daily_table_list:
                    print "daily table existed !!!!!"   
                else:
                    if time_p=="":
                        return "first line userstat!!!"
                    create_new_table_for_daily_active_pass(time_p)
                    daily_table_last = daily_table
                    daily_table_list.append(daily_table)
                ############ 2016 passed end                


                cur,conn= get_pgconn()
                #sql_get_all = "select count(id) from "+daily_table+"  where imsi='" + imsi + "' or imei='" + imei +"' or android_id='"+android_id+"' or wifi_mac='"+wifi_mac+"' and proj_name='"+proj_name+"'"
                sql_get_all = "select count(id) from "+daily_table+"  where imsi='" + imsi + "' or android_id='"+android_id+"' or wifi_mac='"+wifi_mac+"' and proj_name='"+proj_name+"'"
                cur.execute(sql_get_all)
                results_all = cur.fetchall()
                close_pgconn(cur,conn)

                if results_all[0][0]==0:
                    cur,conn = get_pgconn()  
                    sql_insert_act = "insert into "+daily_table+"(imsi,imei,android_id,wifi_mac,date_s,proj_name) values('"+ imsi + "','" + imei + "','" + android_id + "','" + wifi_mac +"','"+time+"','"+proj_name+"')"             
                    cur.execute(sql_insert_act)
                    commit_conn(conn)   
                    close_pgconn(cur,conn)         

                if imsi.count("UNKNOWN")>0 or imei.count("UNKNOWN")>0:
                    cur,conn= get_pgconn()
                    sql_get_all_unk = "select count(id) from "+daily_table+"  where android_id='"+android_id+"' or wifi_mac='"+wifi_mac+"' and proj_name='"+proj_name+"'"
                    cur.execute(sql_get_all_unk)
                    results_all_unk = cur.fetchall()
                    close_pgconn(cur,conn)   

                    if results_all_unk[0][0]==0: 
                        cur,conn = get_pgconn()  
                        sql_insert_act = "insert into "+daily_table+"(imsi,imei,android_id,wifi_mac,date_s,proj_name) values('"+ imsi + "','" + imei + "','" + android_id + "','" + wifi_mac +"','"+time+"','"+proj_name+"')"             
                        cur.execute(sql_insert_act)
                        commit_conn(conn)   
                        close_pgconn(cur,conn) 
            else:
                ############ 2016 passed start
                if i.count(']  INFO -- : [')!=0:
                    time = i[4:14]
                    time_p = time.replace("-","_")
                ############ 2016 passed end      

                # #####
                # if i.count('sub_channel')==0:
                #     # ############ 2016 passed start
                #     # if i.count(']  INFO -- : [')!=0:
                #     #     time = i[4:14]
                #     #     time_p = time.replace("-","_")
                #     # ############ 2016 passed end                
                #     continue
                # else:
                #     ind_imsi = i.find('imsi')
                #     ind_sub_channel = i.find('sub_channel')
                #     ind_sub_channel_id = i.find('sub_channel_id')
                #     ind_mac = i.find('mac_addr')

                #     if ind_imsi==-1 or ind_mac==-1:
                #         continue
                #     else:
                #         imsi = i[ind_imsi+7:ind_imsi+22]

                #         sub_channel_clip = i[ind_sub_channel:-1]
                #         print sub_channel_clip
                #         first_get_yinhao = str(sub_channel_clip).find('"')
                #         again_get_yinhao = sub_channel_clip.find('"',14)
                #         print first_get_yinhao
                #         print again_get_yinhao

                #         sub_channel_name = sub_channel_clip[first_get_yinhao+1:again_get_yinhao]

                #         sub_channel_id_clip = i[ind_sub_channel_id:-1]
                #         # first_get_yinhao_id = sub_channel_id_clip.find['"']
                #         again_get_yinhao_id = sub_channel_id_clip.find(',',17)
                #         sub_channel_id = sub_channel_id_clip[16:again_get_yinhao_id]

                #         wifi_mac = i[ind_mac+11:ind_mac+28]
                        
                #         print sub_channel_id_clip
                #         print sub_channel_id
                #         print sub_channel_name

                #         #info_join = imsi+"$&&&#####"+imei+"$&&&#####"+android_id+"$&&&#####"+wifi_mac

                #         ### calculating independent users
                #         cur,conn= get_pgconn()
                #         sql_update_sub_channel = "update table_activate_num_ids set sub_channel_name='"+sub_channel_name+"',sub_channel_id='" +sub_channel_id + "' where wifi_mac='"+wifi_mac+"'"
                #         cur.execute(sql_update_sub_channel)
                #         commit_conn(conn)   
                #         close_pgconn(cur,conn)   


                #         ### calculating daily active users

                #         now_t = datetime.datetime.now()
                #         now_str_t = now_t.strftime('%Y_%m_%d')
                #         daily_table = "table_daily_active_"+now_str_t
                   
                #         ############ 2016 passed start
                #         daily_table = "table_daily_active_"+time_p
                #         #daily_table_last = daily_table     
                #         if daily_table in daily_table_list:
                #             print "daily table existed !!!!!"   
                #         else:
                #             create_new_table_for_daily_active_pass(time_p)
                #             daily_table_last = daily_table
                #             daily_table_list.append(daily_table)
                #         ############ 2016 passed end                
                #         cur,conn= get_pgconn()
                #         sql_update_sub_channel = "update "+daily_table+" set sub_channel_name='"+sub_channel_name+"',sub_channel_id='" +sub_channel_id + "' where wifi_mac='"+wifi_mac+"'"
                #         cur.execute(sql_update_sub_channel)
                #         commit_conn(conn)   
                #         close_pgconn(cur,conn)                  
                # #####          
                continue       

        f.close()
        #os.remove(f_name_tar + "_files/"+file)      
        count_loop = count_loop + 1

    #os.remove(file_name)
    #os.remove(f_name_tar)
    #shutil.rmtree(f_name_tar + "_files/")


    print daily_table_list

    return "OK"    

def get_all_table_name():
    sql = "select pg_tables.tablename from pg_tables order by pg_tables.tablename"
    cur,conn = get_pgconn()
    cur.execute(sql)
    results = cur.fetchall()
    close_pgconn(cur,conn)   
    
    result_str = []
    for items in results:
        result_str.append(items[0])

    print result_str
    return "OK"

#insert date list into table that holds activated dates
def put_active_datelist_into_db():

    sql_get_tables = "select pg_tables.tablename from pg_tables order by pg_tables.tablename"
    cur,conn= get_pgconn()
    cur.execute(sql_get_tables)
    results_get_tables = cur.fetchall()
    close_pgconn(cur,conn)    

    arr = []
    for item_tables in results_get_tables:
        arr.append(item_tables[0])    

    # arr = ['auth_group', 'auth_group_permissions', 'auth_permission', 'auth_user', 'auth_user_groups', 'auth_user_user_permissions', 'django_admin_log', 'django_content_type', 'django_migrations', 'django_session', 'pg_aggregate', 'pg_am', 'pg_amop', 'pg_amproc', 'pg_attrdef', 'pg_attribute', 'pg_auth_members', 'pg_authid', 'pg_cast', 'pg_class', 'pg_collation', 'pg_constraint', 'pg_conversion', 'pg_database', 'pg_db_role_setting', 'pg_default_acl', 'pg_depend', 'pg_description', 'pg_enum', 'pg_event_trigger', 'pg_extension', 'pg_foreign_data_wrapper', 'pg_foreign_server', 'pg_foreign_table', 'pg_index', 'pg_inherits', 'pg_language', 'pg_largeobject', 'pg_largeobject_metadata', 'pg_namespace', 'pg_opclass', 'pg_operator', 'pg_opfamily', 'pg_pltemplate', 'pg_policy', 'pg_proc', 'pg_range', 'pg_replication_origin', 'pg_rewrite', 'pg_seclabel', 'pg_shdepend', 'pg_shdescription', 'pg_shseclabel', 'pg_statistic', 'pg_tablespace', 'pg_transform', 'pg_trigger', 'pg_ts_config', 'pg_ts_config_map', 'pg_ts_dict', 'pg_ts_parser', 'pg_ts_template', 'pg_type', 'pg_user_mapping', 'sql_features', 'sql_implementation_info', 'sql_languages', 'sql_packages', 'sql_parts', 'sql_sizing', 'sql_sizing_profiles', 'table_activate_date_list', 'table_activate_num', 'table_activate_num_daily_total', 'table_activate_num_fake', 'table_activate_num_ids', 'table_country_list', 'table_daily_active_2016_05_29', 'table_daily_active_2016_05_30', 'table_daily_active_2016_05_31', 'table_daily_active_2016_06_10', 'table_daily_active_2016_06_11', 'table_daily_active_2016_06_12', 'table_daily_active_2016_06_13', 'table_daily_active_2016_06_14', 'table_daily_active_2016_06_15', 'table_daily_active_2016_06_16', 'table_daily_active_2016_06_17', 'table_daily_active_2016_06_18', 'table_daily_active_2016_06_19', 'table_daily_active_2016_06_20', 'table_daily_active_2016_06_21', 'table_daily_active_2016_06_22', 'table_daily_active_2016_06_23', 'table_daily_active_2016_06_24', 'table_daily_active_2016_06_25', 'table_daily_active_2016_06_26', 'table_daily_active_2016_06_27', 'table_daily_active_2016_06_28', 'table_daily_active_2016_06_29', 'table_daily_active_2016_06_30', 'table_daily_active_2016_07_01', 'table_daily_active_2016_07_02', 'table_daily_active_2016_07_03', 'table_daily_active_2016_07_04', 'table_daily_active_2016_07_05', 'table_daily_active_2016_07_06', 'table_daily_active_2016_07_07', 'table_daily_active_2016_07_08', 'table_daily_active_2016_07_09', 'table_daily_active_2016_08_29', 'table_daily_active_2016_08_30', 'table_daily_active_2016_09_03', 'table_daily_active_2016_09_04', 'table_daily_active_2016_09_05', 'table_daily_active_2016_09_06', 'table_daily_active_2016_09_13', 'table_daily_active_2016_09_14', 'table_daily_active_2016_11_22', 'table_daily_active_2016_11_23', 'table_daily_active_2016_11_28', 'table_daily_active_2016_12_05', 'table_daily_active_2016_12_06', 'table_daily_active_2016_12_14', 'table_daily_active_2016_12_18', 'table_daily_active_2016_12_19', 'table_daily_active_2016_12_27', 'table_daily_active_2016_12_28', 'table_daily_active_2016_12_29', 'table_daily_active_2016_12_30', 'table_daily_active_2017_01_07', 'table_daily_active_2017_01_08', 'table_daily_active_2017_01_12', 'table_daily_active_2017_01_13', 'table_daily_active_2017_01_21', 'table_daily_active_2017_01_22', 'table_daily_active_2017_01_23', 'table_daily_active_2017_01_24', 'table_daily_active_2017_01_25', 'table_daily_active_2017_02_13', 'table_daily_active_2017_02_14', 'table_login_time', 'table_menues', 'table_permission', 'table_proj', 'table_role', 'table_user']

    for item in arr:
        if item.count("table_daily_active_")!=0:
            sql_get_existance = "select id from table_activate_date_list where date_s='"+str(item[19:29])+"' and "
            cur,conn = get_pgconn()
            cur.execute(sql_get_existance)
            results_get_existance = cur.fetchall()
            close_pgconn(cur,conn)    
                
            if results_get_existance==[]:
                sql = "insert into table_activate_date_list(date_s) values('"+str(item[19:29])+"')"
                print sql
                cur,conn = get_pgconn()
                cur.execute(sql)
                commit_conn(conn)   
                close_pgconn(cur,conn)

    return "OK"   

#insert active daily num for 2016
def put_daily_active_total_2016():
    sql_get_date_list = "select date_s from table_activate_date_list"
    cur,conn = get_pgconn()
    cur.execute(sql_get_date_list)
    results_get_date_list = cur.fetchall()
    close_pgconn(cur,conn)  

    for item in results_get_date_list:
        table_name = "table_daily_active_"+item[0]
        date_replace = item[0].replace("_","-")

        sql_get_existance = "select id from table_activate_num_daily_total where date_s='"+date_replace+"' and sub_channel_name="
        cur,conn = get_pgconn()
        cur.execute(sql_get_existance)
        results_get_existance = cur.fetchall()
        close_pgconn(cur,conn) 

        if results_get_existance==[]:
            sql_get_num = "select count(id) from "+table_name

            cur,conn = get_pgconn()
            cur.execute(sql_get_num)
            results_sql_get_num = cur.fetchall()
            close_pgconn(cur,conn)  

            sql = "insert into table_activate_num_daily_total(date_s,proj_name,total_num,sub_channel_name) values('"+date_replace+"','Tripics',"+str(results_sql_get_num[0][0])+")"
            cur,conn = get_pgconn()
            cur.execute(sql)
            commit_conn(conn)   
            close_pgconn(cur,conn)

    return "OK"

#put total_active II
def put_total_active_II():    

    cur,conn= get_pgconn()
    sql = "select pg_tables.tablename from pg_tables  where pg_tables.tablename like 'table_daily_active_%' order by pg_tables.tablename"
    cur.execute(sql)
    results = cur.fetchall()
    close_pgconn(cur,conn) 

    for item in results:
        date = item[0][19:].replace("_","-")
        sql_get_total_by_subchannel = "select count(a.id),b.sub_channel_name from " + item[0] + "  a join table_activate_num_ids b on a.wifi_mac=b.wifi_mac where b.sub_channel_name!='' group by b.sub_channel_name"
        cur,conn= get_pgconn()
        cur.execute(sql_get_total_by_subchannel)
        results_get_total_by_subchannel = cur.fetchall()
        close_pgconn(cur,conn)
        print sql_get_total_by_subchannel

        for item_fff in results_get_total_by_subchannel:
            sql_get_total_by_subchannel_exe = "select id from table_activate_num_daily_total where date_s='"+date+"' and sub_channel_name='" +item_fff[1]+"'"
            cur,conn= get_pgconn()
            cur.execute(sql_get_total_by_subchannel_exe)
            results_get_total_by_subchannel_exe = cur.fetchall()
            close_pgconn(cur,conn) 

            if results_get_total_by_subchannel_exe==[]:
                cur,conn= get_pgconn()
                sql_in = "insert into table_activate_num_daily_total(date_s,proj_name,total_num,sub_channel_name) values('"+date+"','Tripics','"+str(item_fff[0])+"','"+item_fff[1]+"')"
                cur.execute(sql_in)
                commit_conn(conn)   
                close_pgconn(cur,conn)                           

    return "OK"

#insert daily active total count for every project to database ,and delete the table for today
def insert_all_daily_data():
    now_t = datetime.datetime.now()
    now_str_t = now_t.strftime('%Y-%m-%d')
    daily_table = "table_daily_active_"+now_str_t

    cur,conn= get_pgconn()
    sql = "select count(id) cnt,proj_name from "+daily_table+" group by proj_name"
    cur.execute(sql)
    results_total_daily = cur.fetchall()
    close_pgconn(cur,conn) 

    for i in results_total_daily:
        cur,conn= get_pgconn()
        sql_in = "insert into table_activate_num_daily_total(date_s,proj_name,total_num) values('"+now_str_t+"','"+i[1]+"',"+str(i[0])+")"
        cur.execute(sql_in)
        commit_conn(conn)   
        close_pgconn(cur,conn)           
    ###

    ### delete daily table 
    # cur,conn= get_pgconn()
    # sql_tun = "truncate "+daily_table
    # cur.execute(sql_tun)
    # commit_conn(conn)   
    # close_pgconn(cur,conn)

    return "OK"  

#get user type
def get_user_type(user_name):
    sql = "select user_type from table_user where user_name='"+user_name+"'"
    cur,conn = get_pgconn()
    cur.execute(sql)
    results = cur.fetchall()
    close_pgconn(cur,conn)

    print results[0][0]
    return results[0][0]

#get user info
def get_user_info_list(user_name, name_filter):

    result_str = ""

    if name_filter=="":
        sql = "select id ,user_name,last_login_time, user_type , comment, status, related_projs from table_user"
    else:
        sql = "select id ,user_name,last_login_time, user_type , comment, status, related_projs from table_user where user_name like '%"+name_filter+"%'"

    sql_get_user_type = "select user_type from table_user where user_name='"+user_name+"'"

    cur,conn = get_pgconn()
    cur.execute(sql_get_user_type)
    results_get_user_type = cur.fetchall()
    close_pgconn(cur,conn)

    print results_get_user_type[0][0]
    if results_get_user_type[0][0]!='超级管理员':
        sql = "select id ,user_name,last_login_time, user_type, comment, status, related_projs from table_user where user_name='"+user_name+"'"

    cur,conn = get_pgconn()
    cur.execute(sql)
    results = cur.fetchall()
    close_pgconn(cur,conn)

    if results!=[]:
        for item in results:
            each_result = {}
            each_result['id'] = item[0]
            each_result['user_name'] = item[1]
            #print each_result['title']
            #print type(each_result['title'])       
            each_result['last_login_time'] = item[2]  
            if item[3]=='super_admin':
                each_result['user_type'] = "超级管理员"
            elif item[3]=='admin':
                each_result['user_type'] = "管理员"
            elif item[3]=='commercial':
                each_result['user_type'] = "商务"
            elif item[3]=='client':
                each_result['user_type'] = "客户"

            each_result['user_type'] = item[3]  
            each_result['comment'] = item[4]
            each_result['state'] = item[5]
            #each_result['rate'] = item[2] 
            #result_str_each = each_result['title'] + "," + each_result['number']
            #result_item.append(each_result)

            #each_result['lively_num'] = int(results[0][0]*each_result['rate'])      
            if item[3]!='客户' and item[3]!='商务':   
                proj_col = "99999999"   
            else:
                proj_col = item[6]   
            if str(proj_col) != "None":
                print str(proj_col)
                #proj_col = ""
                sql_get_projs = "select proj_name from table_proj where id in ("+proj_col+")"

                cur,conn = get_pgconn()
                cur.execute(sql_get_projs)
                results_get_projs = cur.fetchall()
                close_pgconn(cur,conn)

                projs_str = ""
                for i in results_get_projs:
                    projs_str = projs_str + i[0] + ","

                projs_str = projs_str[0:int(len(projs_str))-1]
            else:
                projs_str = " "
            
            if item[3] == "超级管理员" or item[3] == "管理员":
                projs_str = "所有"
            # print "projs "
            # print results_get_user_type[0][0]
            # print sql_get_projs
            # print projs_str
            sql_get_logintime = "select login_time from table_login_time where user_name='"+item[1]+"' order by id desc limit 1"

            cur,conn = get_pgconn()
            cur.execute(sql_get_logintime)
            results_get_logintime = cur.fetchall()
            close_pgconn(cur,conn)          
            print sql_get_logintime
            if results_get_logintime!=[]:
                each_result['last_login_time'] = results_get_logintime[0][0]
            else:
                each_result['last_login_time'] = " "                

            result_str = result_str+'{"id":"' + str(each_result['id']) +'",'+'"user_name":"' + str(each_result['user_name']) + '","last_login_time":"' + str(each_result['last_login_time'])  + '",'+'"user_type":"' + item[3]+'","comment":"' + item[4]+'","state":"' + item[5]+'","projs":"'+projs_str+'"'+'},'      

    result_str = result_str[0:int(len(result_str))-1]    
    result_str = '{"allData":[' + result_str +']}'        
    #print result_item
    #return HttpResponse("<p>"+str(result_item)+"</p>")
    print result_str
    return result_str  

#put logintime into database
def put_logintime(user_name):
    now_t = datetime.datetime.now()
    now_str_t = now_t.strftime('%Y-%m-%d %H:%M:%S')

    #获取本机电脑名
    myname = socket.getfqdn(socket.gethostname(  ))
    #获取本机ip
    myaddr = socket.gethostbyname(myname) 
  
    sql = "insert into table_login_time(user_name,login_time,ip) values('"+user_name+"','"+now_str_t+"','"+myaddr+"')"
    cur,conn= get_pgconn()
    # sql_in = "insert into table_activate_num_daily_total(date_s,proj_name,total_num) values('"+now_str_t+"','"+i[1]+"',"+str(i[0])+")"
    cur.execute(sql)
    commit_conn(conn)   
    close_pgconn(cur,conn) 

    return "OK"
#get logintime list
def get_user_logintime_list(user_name):
    result_str = ""

    sql = "select login_time ,ip from table_login_time where user_name='"+ user_name +"' order by login_time desc"
    # if name_filter=="":
    #     sql = "select id ,user_name,last_login_time, user_type , comment, status, related_projs from table_user"
    # else:
    #     sql = "select id ,user_name,last_login_time, user_type , comment, status, related_projs from table_user where user_name like '%"+name_filter+"%'"

    # sql_get_user_type = "select user_type from table_user where user_name='"+user_name+"'"

    # cur,conn = get_pgconn()
    # cur.execute(sql_get_user_type)
    # results_get_user_type = cur.fetchall()
    # close_pgconn(cur,conn)

    # if results_get_user_type[0][0]!='超级管理员':
    #     sql = "select id ,user_name,last_login_time, user_type, comment, status, related_projs from table_user where user_name='"+user_name+"'"

    cur,conn = get_pgconn()
    cur.execute(sql)
    results = cur.fetchall()
    close_pgconn(cur,conn)

    if results!=[]:
        for item in results:
            each_result = {}
            each_result['id'] = item[0]
            each_result['user_name'] = item[1]
            #print each_result['title']
            #print type(each_result['title'])       
            # each_result['last_login_time'] = item[2]  
            # if item[3]=='super_admin':
            #     each_result['user_type'] = "超级管理员"
            # elif item[3]=='admin':
            #     each_result['user_type'] = "管理员"
            # elif item[3]=='commercial':
            #     each_result['user_type'] = "商务"
            # elif item[3]=='client':
            #     each_result['user_type'] = "客户"

            each_result['login_time'] = item[0]  
            each_result['ip'] = item[1]
            # each_result['state'] = item[5]
            #each_result['rate'] = item[2] 
            #result_str_each = each_result['title'] + "," + each_result['number']
            #result_item.append(each_result)

            #each_result['lively_num'] = int(results[0][0]*each_result['rate'])      
            # if item[3]!='客户' and item[3]!='商务':   
            #     proj_col = "99999999"   
            # else:
            #     proj_col = item[6]   
            # sql_get_projs = "select proj_name from table_proj where id in ("+proj_col+")"

            # cur,conn = get_pgconn()
            # cur.execute(sql_get_projs)
            # results_get_projs = cur.fetchall()
            # close_pgconn(cur,conn)

            # projs_str = ""
            # for i in results_get_projs:
            #     projs_str = projs_str + i[0] + ","

            # projs_str = projs_str[0:int(len(projs_str))-1]

            # # print "projs "
            # # print results_get_user_type[0][0]
            # # print sql_get_projs
            # # print projs_str
            # sql_get_logintime = "select login_time from table_login_time where user_name='"+item[1]+"' order by id desc limit 1"

            # cur,conn = get_pgconn()
            # cur.execute(sql_get_logintime)
            # results_get_logintime = cur.fetchall()
            # close_pgconn(cur,conn)          
            # print sql_get_logintime
            # if results_get_logintime!=[]:
            #     each_result['last_login_time'] = results_get_logintime[0][0]
            # else:
            #     each_result['last_login_time'] = " "                

            if str(each_result['ip'])=="None":
               each_result['ip'] = " "

            result_str = result_str+'{"login_time":"' + str(each_result['login_time']) +'",'+'"ip":"' + str(each_result['ip']) + '"'+'},'      

    result_str = result_str[0:int(len(result_str))-1]    
    result_str = '{"allData":[' + result_str +']}'        
    #print result_item
    #return HttpResponse("<p>"+str(result_item)+"</p>")
    print result_str
    return result_str  

#change passwd
def change_passwd(user_name, passwd):
    sql = "update table_user set passwd='"+passwd+"' where user_name='"+user_name+"'"
    cur,conn= get_pgconn()
    ##sql_in = "insert into table_activate_num_daily_total(date_s,proj_name,total_num) values('"+now_str_t+"','"+i[1]+"',"+str(i[0])+")"
    cur.execute(sql)
    commit_conn(conn)   
    close_pgconn(cur,conn)    

    return "OK"

#change role
def change_role(user_name, role):
    sql = "update table_user set user_type='"+role+"' where user_name='"+user_name+"'"
    cur,conn= get_pgconn()
    ##sql_in = "insert into table_activate_num_daily_total(date_s,proj_name,total_num) values('"+now_str_t+"','"+i[1]+"',"+str(i[0])+")"
    cur.execute(sql)
    commit_conn(conn)   
    close_pgconn(cur,conn)    

    return "OK"

#change comment for user
def change_comment(user_name, comment):
    sql = "update table_user set comment='"+comment+"' where user_name='"+user_name+"'"
    cur,conn= get_pgconn()
    ##sql_in = "insert into table_activate_num_daily_total(date_s,proj_name,total_num) values('"+now_str_t+"','"+i[1]+"',"+str(i[0])+")"
    cur.execute(sql)
    commit_conn(conn)   
    close_pgconn(cur,conn)    

    return "OK"    

#get role info
def get_role_info():
    sql = "select id, role from table_role"
    cur,conn = get_pgconn()
    cur.execute(sql)
    results = cur.fetchall()
    close_pgconn(cur,conn)

    result_str = ""
    if results!=[]:
        result_str = result_str+'{"role":"' + results[0][0] + '"},'

    result_str = result_str[0:int(len(result_str))-1]    
    result_str = '{"allData":[' + result_str +']}'    

    print result_str
    return result_str    

#froze account
def froze_accout(user_name):
    sql = "update table_user set status='冻结' where user_name='"+user_name+"'"    
    cur,conn= get_pgconn()
    ##sql_in = "insert into table_activate_num_daily_total(date_s,proj_name,total_num) values('"+now_str_t+"','"+i[1]+"',"+str(i[0])+")"
    cur.execute(sql)
    commit_conn(conn)   
    close_pgconn(cur,conn)    

    return "OK"    

# def get_projs():
#     sql = "select proj_id,proj_name from table_proj order by proj_id"
#     cur,conn = get_pgconn()
#     cur.execute(sql)
#     results = cur.fetchall()
#     close_pgconn(cur,conn)

#     result_str = ""
#     if results!=[]:
#         for item  in results:
#             # result_str = result_str+'{"proj_id":"' + str(item[0]) + '","proj_name":"'+ str(item[1]) +'"},'
#             result_str = result_str + '"'+str(item[1]) +'",'

#     result_str = result_str[0:int(len(result_str))-1]    
#     result_str = '{"allData":[' + result_str +']}' 

#     print result_str
#     return result_str   

def get_projs():
    sql = "select distinct sub_channel_name from table_activate_num_ids where  sub_channel_name!=''"
    cur,conn = get_pgconn()
    cur.execute(sql)
    results = cur.fetchall()
    close_pgconn(cur,conn)

    result_str = ""
    if results!=[]:
        for item  in results:
            # result_str = result_str+'{"proj_id":"' + str(item[0]) + '","proj_name":"'+ str(item[1]) +'"},'
            result_str = result_str + '"'+str(item[0]) +'",'

    result_str = result_str[0:int(len(result_str))-1]    
    result_str = '{"allData":[' + result_str +']}' 

    print result_str
    return result_str  

#change related project
def change_related_project(user_name, arr_projs):
    print "changing!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    print arr_projs
    sql_get_user_former_info = "select user_type, passwd, last_login_time, status ,comment  from table_user where user_name='"+user_name+"' limit 1"
    cur,conn = get_pgconn()
    #sql_get_type = "select user_type from table_user where user_name='"+user_name+"'"
    cur.execute(sql_get_user_former_info)
    results_get_user_former_info = cur.fetchall()
    close_pgconn(cur,conn)

    sql_delete_former = "delete from table_user where user_name='"+user_name+"'"
    cur,conn= get_pgconn()
    ##sql_in = "insert into table_activate_num_daily_total(date_s,proj_name,total_num) values('"+now_str_t+"','"+i[1]+"',"+str(i[0])+")"
    cur.execute(sql_delete_former)
    commit_conn(conn)   
    close_pgconn(cur,conn)      

    arr_projs_str = ""
    arr_str_sp = arr_projs.split(",")
    for i in arr_str_sp:
        
        
        print "dfddfdfdfdfdfdfd"
        print i
        sql_get_proj_id = "select proj_id  from table_proj where proj_name='"+str(i)+"' limit 1"
        cur,conn = get_pgconn()
        #sql_get_type = "select user_type from table_user where user_name='"+user_name+"'"
        cur.execute(sql_get_proj_id)
        results_get_proj_id = cur.fetchall()
        close_pgconn(cur,conn)

        arr_projs_str = arr_projs_str + str(results_get_proj_id[0][0])+","
        results_get_proj_id


    arr_projs_str = arr_projs_str[0:int(len(arr_projs_str))-1]  

    # arr_projs_str

    la_l = results_get_user_former_info[0][2]
    if str(results_get_user_former_info[0][2])=="None":
        la_l = ""
    
    status = results_get_user_former_info[0][3]
    comment = results_get_user_former_info[0][4]
    print user_name
    print results_get_user_former_info[0][0]
    print results_get_user_former_info[0][1]
    print arr_projs_str
    print results_get_user_former_info[0][2]
    print status

    sql_insert_new = "insert into table_user(user_name,user_type,passwd, related_projs, last_login_time,status,comment) values('"+user_name+"','"+results_get_user_former_info[0][0]+"','"+results_get_user_former_info[0][1]+"','"+arr_projs_str+"','"+la_l+"','"+status+"','"+comment+"')"
    cur,conn= get_pgconn()
    cur.execute(sql_insert_new)
    commit_conn(conn)   
    close_pgconn(cur,conn)

    return "OK"          

#get role-menu info 
def get_rolemenues_info():
    sql = "select id,role_name,related_menues from table_role"
    cur,conn = get_pgconn()
    cur.execute(sql)
    results = cur.fetchall()
    close_pgconn(cur,conn)

    #if results!=[]:
    #for each_role in results:

    result_str = ""
    if results!=[]:
        for item in results:
            #each_result['role'] = item[0]
            #each_result['active'] = results_get_dailyactive[0][1]
            #print each_result['title']
            #print type(each_result['title'])       
            #each_result['duli'] = item[1]   
            #each_result['rate'] = item[2] 
            #result_str_each = each_result['title'] + "," + each_result['number']
            #result_item.append(each_result)   
            
            
            sql_menu_names = "select id,menu_name from table_menues where id in (" + str(item[2]) +")"
            cur,conn = get_pgconn()
            cur.execute(sql_menu_names)
            results_menu_names = cur.fetchall()
            close_pgconn(cur,conn)

            menu_names_str = ""
            for itemtt in results_menu_names:
                menu_names_str = menu_names_str + itemtt[1]+","
            menu_names_str = menu_names_str[0:int(len(menu_names_str))-1]

            result_str = result_str+'{"role":"' + item[1] + '","menues":"'+ menu_names_str+ '"},'

    result_str = result_str[0:int(len(result_str))-1]    
    result_str = '{"allData":[' + result_str +']}'    

    print result_str
    return result_str      
    #return "OK"

#interface to get tongji data to frontpage
def get_tongji_to_frontpage(user_name,date_1,date_2,proj):

    # print date_1
    # print date_2
    #print date_range

    date_range_array=[]
    date_range_array.append(date_1)
    date_range_array.append(date_2)
    date_range_box = []
    date_from = ""
    date_to = ""

    fil = False

    if date_1!="undefined" and date_1!="" and date_2!="undefined" and date_2!="" and date_1!="first" and date_2!="first":
        fil = True
        for j in date_range_array:
            date_array = j.split(' ')
            month = date_array[1]
            day = date_array[2]
            year = date_array[3]
            if month == 'Jan':
                month = '01'
            elif month == 'Feb':
                month = '02' 
            elif month == 'Mar':
                month = '03' 
            elif month == 'Apr':
                month = '04'             
            elif month == 'May':
                month = '05'     
            elif month == 'Jun':
                month = '06' 
            elif month == 'Jul':
                month = '07' 
            elif month == 'Aug':
                month = '08'             
            elif month == 'Sep':
                month = '09'   
            elif month == 'Oct':
                month = '10' 
            elif month == 'Nov':
                month = '11'             
            elif month == 'Dec':
                month = '12' 
            formatted_date = year +"-"+ month +"-"+ day
            date_range_box.append(formatted_date)

        date_from = date_range_box[0]
        date_to = date_range_box[1]
    else:
        now = datetime.datetime.now()
        one_week_ago = now - datetime.timedelta(days=7)
        date_str = now.strftime('%Y-%m-%d') 
        date_str_one_week_ago = one_week_ago.strftime('%Y-%m-%d')  
        date_from = date_str_one_week_ago
        date_to = date_str

    # print date_from
    # print date_to

    cur,conn = get_pgconn()
    sql_get_type = "select user_type ,related_projs from table_user where user_name='"+user_name+"'"
    cur.execute(sql_get_type)
    results_get_type = cur.fetchall()
    close_pgconn(cur,conn) 

    # print "fdddd"
    # print str(results_get_type[0][1])

    if str(results_get_type[0][1])!="None":
        proj_id_col = "("+results_get_type[0][1]+")"
    else:
        proj_id_col = "nothing"

    # ######get total duli begin
    # if results_get_type[0][0]=='客户' or results_get_type[0][0]=='商务':
    #     # group by date
    #     # sql_get_totalduli_ids = "select c.proj_name,count(c.id) from table_proj b  join table_activate_num_ids c on b.proj_name=c.proj_name  where b.proj_id in "+proj_id_col+" and c.proj_name='"+item[0]+"' group by c.proj_name"                 
    #     sql_get_totalduli_ids = "select count(c.id) from table_proj b  join table_activate_num_ids c on b.proj_name=c.proj_name  where c.date_s<='" +date_to+"'"
    # else:
    #     # group by date
    #     # sql_get_totalduli_ids = "select c.proj_name,count(c.id) from table_activate_num_ids c  where c.proj_name='"+item[0]+"' group by c.proj_name"  
    #     sql_get_totalduli_ids = "select count(c.id) from table_activate_num_ids c  where c.date_s<='" +date_to+"'"
        
    # cur,conn = get_pgconn()
    # cur.execute(sql_get_totalduli_ids)
    # results_get_totalduli_ids = cur.fetchall()
    # close_pgconn(cur,conn)  

    # if results_get_totalduli_ids!=[]:
    #     total_duli_s = results_get_totalduli_ids[0][0]
    # else:
    #     total_duli_s = 0

    # ######get total duli over

    if results_get_type[0][0]=='客户' or results_get_type[0][0]=='商务':
        # group by date 
        # sql_get_duli_ids = "select c.proj_name,count(c.id) from table_proj b  join table_activate_num_ids c on b.proj_name=c.proj_name  where b.proj_id in "+proj_id_col+" and c.date_s>='"+date_from+"' and c.date_s<='" +date_to+ "' group by c.proj_name"
        sql_get_duli_ids = "select c.date_s,count(c.id) from table_proj b  join table_activate_num_ids c on b.proj_name=c.proj_name  where b.proj_id in "+proj_id_col+" and c.date_s>='"+date_from+"' and c.date_s<='" +date_to+ "'  group by c.date_s order  by c.date_s desc"
 
    else:
        # group by date
        # sql_get_duli_ids = "select c.proj_name,count(c.id) from table_activate_num_ids c  where c.date_s>='"+date_from+"' and c.date_s<='" +date_to+ "' group by c.proj_name"
        sql_get_duli_ids = "select c.date_s,count(c.id) from table_activate_num_ids c  where c.date_s>='"+date_from+"' and c.date_s<='" +date_to+ "' group by c.date_s order by c.date_s desc"

    cur,conn = get_pgconn()
    #sql_get_act = "select proj_name,date_s,act_num from table_activate_num where proj_id=" + str(proj_id)+" and date_s>='"+date_from+"' and date_s<='" +date_to+ "' order by date_s desc"
    cur.execute(sql_get_duli_ids)
    # print sql_get_duli_ids
    results_get_duli_ids = cur.fetchall()
    close_pgconn(cur,conn)        

    result_item = []
    result_str = ""
    
    if results_get_duli_ids!=[]:
        for index,item in enumerate(results_get_duli_ids):

            if results_get_type[0][0]=='客户' or results_get_type[0][0]=='商务':
                # group by date
                # sql_get_dailyactive = "select c.proj_name,sum(c.total_num) from table_proj b  join table_activate_num_daily_total c on b.proj_name=c.proj_name  where b.proj_id in "+proj_id_col+" and c.date_s>='"+date_from+"' and c.date_s<='" +date_to+"' and c.proj_name='"+item[0]+ "' group by c.proj_name"                
                sql_get_dailyactive = "select c.date_s,sum(c.total_num) from table_proj b  join table_activate_num_daily_total c on b.proj_name=c.proj_name  where c.date_s='"+item[0]+"' and b.proj_id in "+proj_id_col+" and c.date_s>='"+date_from+"' and c.date_s<='" +date_to+"'  group by c.date_s order  by c.date_s desc"
            else:
                # group by date
                # sql_get_dailyactive = "select c.proj_name,sum(c.total_num) from table_activate_num_daily_total c where c.date_s>='"+date_from+"' and c.date_s<='" +date_to+"' and c.proj_name='"+item[0]+"' group by c.proj_name "                
                sql_get_dailyactive = "select c.date_s,sum(c.total_num) from table_activate_num_daily_total c where  c.date_s='"+item[0]+"' and  c.date_s>='"+date_from+"' and c.date_s<='" +date_to+"'  group by c.date_s  order  by c.date_s desc"

            cur,conn = get_pgconn()
            #sql_get_act = "select proj_name,date_s,act_num from table_activate_num where proj_id=" + str(proj_id)+" and date_s>='"+date_from+"' and date_s<='" +date_to+ "' order by date_s desc"
            cur.execute(sql_get_dailyactive)
            #print sql_get_dailyactive
            results_get_dailyactive = cur.fetchall()
            close_pgconn(cur,conn)    


            each_result = {}
            # group by date
            # each_result['proj_name'] = item[0]
            each_result['proj_name'] = "Tripics"
            if results_get_dailyactive!=[]:
                each_result['active'] = results_get_dailyactive[0][1]
            else:
                each_result['active'] = 0
            #print each_result['title']
            #print type(each_result['title'])       
            each_result['duli'] = item[1]   
            #each_result['rate'] = item[2] 
            #result_str_each = each_result['title'] + "," + each_result['number']
            result_item.append(each_result)

            #each_result['lively_num'] = int(results[0][0]*each_result['rate'])      
            if results_get_type[0][0]=='客户' or results_get_type[0][0]=='商务':
                # group by date
                # sql_get_totalactive = "select c.proj_name,sum(c.total_num) from table_proj b  join table_activate_num_daily_total c on b.proj_name=c.proj_name  where b.proj_id in "+proj_id_col+" and c.proj_name='"+item[0]+ "' group by c.proj_name"
                sql_get_totalactive = "select c.date_s,sum(c.total_num) from table_proj b  join table_activate_num_daily_total c on b.proj_name=c.proj_name  where b.proj_id in "+proj_id_col+"  group by c.date_s order  by c.date_s desc"                
            else:
                # group by date
                # sql_get_totalactive = "select c.proj_name,sum(c.total_num) from table_activate_num_daily_total c where c.proj_name='"+item[0]+"' group by c.proj_name "                
                sql_get_totalactive = "select c.date_s,sum(c.total_num) from table_activate_num_daily_total c group by c.date_s  order  by c.date_s desc"            

            cur,conn = get_pgconn()
            #sql_get_act = "select proj_name,date_s,act_num from table_activate_num where proj_id=" + str(proj_id)+" and date_s>='"+date_from+"' and date_s<='" +date_to+ "' order by date_s desc"
            cur.execute(sql_get_totalactive)
            #print sql_get_totalactive
            results_get_totalactive = cur.fetchall()
            close_pgconn(cur,conn)  

            each_result['total_active'] = results_get_totalactive[0][1]

            ######get total duli begin
            if results_get_type[0][0]=='客户' or results_get_type[0][0]=='商务':
                # group by date
                # sql_get_totalduli_ids = "select c.proj_name,count(c.id) from table_proj b  join table_activate_num_ids c on b.proj_name=c.proj_name  where b.proj_id in "+proj_id_col+" and c.proj_name='"+item[0]+"' group by c.proj_name"                 
                sql_get_totalduli_ids = "select count(c.id) from table_proj b  join table_activate_num_ids c on b.proj_name=c.proj_name  where c.date_s<='" +str(item[0])+"'"
            else:
                # group by date
                # sql_get_totalduli_ids = "select c.proj_name,count(c.id) from table_activate_num_ids c  where c.proj_name='"+item[0]+"' group by c.proj_name"  
                sql_get_totalduli_ids = "select count(c.id) from table_activate_num_ids c  where c.date_s<='" +str(item[0])+"'"
                
            cur,conn = get_pgconn()
            cur.execute(sql_get_totalduli_ids)
            results_get_totalduli_ids = cur.fetchall()
            close_pgconn(cur,conn)  

            if results_get_totalduli_ids!=[]:
                total_duli_s = results_get_totalduli_ids[0][0]
            else:
                total_duli_s = 0

            ######get total duli over

            result_str = result_str+'{"proj_name":"' + each_result['proj_name'] +'",'+'"daily_active":"' + str(each_result['active']) + '","duli":"' + str(each_result['duli']) +'",' + '"total_active":"'+str(each_result['total_active']) + '","total_duli":"'+ str(total_duli_s) +'","date":"'+str(item[0])+'","sub_channel_name":"'+"Tripics"+'"},'
    else:
        if results_get_type[0][0]=='客户' or results_get_type[0][0]=='商务':
            sql_get_today_none = "select b.proj_name from table_proj b where b.proj_id in "+proj_id_col
        else:
            sql_get_today_none = "select b.proj_name from table_proj b"

        cur,conn = get_pgconn()
        cur.execute(sql_get_today_none)
        results_get_today_none = cur.fetchall()
        close_pgconn(cur,conn)        

        if results_get_today_none!=[]:
            for item in results_get_today_none:            
                if results_get_type[0][0]=='客户' or results_get_type[0][0]=='商务':
                    # group by date
                    # sql_get_dailyactive = "select c.proj_name,sum(c.total_num) from table_proj b  join table_activate_num_daily_total c on b.proj_name=c.proj_name  where b.proj_id in "+proj_id_col+" and c.date_s>='"+date_from+"' and c.date_s<='" +date_to+"' and c.proj_name='"+item[0]+ "' group by c.proj_name"
                    sql_get_dailyactive = "select c.date_s,sum(c.total_num) from table_proj b  join table_activate_num_daily_total c on b.proj_name=c.proj_name  where  c.date_s='"+item[0]+"' and b.proj_id in "+proj_id_col+" and c.date_s>='"+date_from+"' and c.date_s<='" +date_to+"' group by c.date_s order  by c.date_s desc"                    
                else:
                    # group by date
                    # sql_get_dailyactive = "select c.proj_name,sum(c.total_num) from table_activate_num_daily_total c where c.date_s>='"+date_from+"' and c.date_s<='" +date_to+"' and c.proj_name='"+item[0]+"' group by c.proj_name "    
                    sql_get_dailyactive = "select c.date_s,sum(c.total_num) from table_activate_num_daily_total c where c.date_s='"+item[0]+"' and  c.date_s>='"+date_from+"' and c.date_s<='" +date_to+"'  group by c.date_s  order  by c.date_s desc"                             

                cur,conn = get_pgconn()
                #sql_get_act = "select proj_name,date_s,act_num from table_activate_num where proj_id=" + str(proj_id)+" and date_s>='"+date_from+"' and date_s<='" +date_to+ "' order by date_s desc"
                cur.execute(sql_get_dailyactive)
                #print sql_get_dailyactive
                results_get_dailyactive = cur.fetchall()
                close_pgconn(cur,conn)    


                each_result = {}
                # group by date
                # each_result['proj_name'] = item[0]
                each_result['proj_name'] = "Tripics"
                if results_get_dailyactive!=[]:
                    each_result['active'] = results_get_dailyactive[0][1]
                else:
                    each_result['active'] = 0
                #print each_result['title']
                #print type(each_result['title'])       
                each_result['duli'] = 0   
                #each_result['rate'] = item[2] 
                #result_str_each = each_result['title'] + "," + each_result['number']
                result_item.append(each_result)

                #each_result['lively_num'] = int(results[0][0]*each_result['rate'])      

                if results_get_type[0][0]=='客户' or results_get_type[0][0]=='商务':
                    # group by date
                    # sql_get_totalactive = "select c.proj_name,sum(c.total_num) from table_proj b  join table_activate_num_daily_total c on b.proj_name=c.proj_name  where b.proj_id in "+proj_id_col+" and c.proj_name='"+item[0]+ "' group by c.proj_name"
                    sql_get_totalactive = "select c.date_s,sum(c.total_num) from table_proj b  join table_activate_num_daily_total c on b.proj_name=c.proj_name  where b.proj_id in "+proj_id_col+"  group by c.date_s order by c.date_s desc"                    
                else:
                    # group by date
                    # sql_get_totalactive = "select c.proj_name,sum(c.total_num) from table_activate_num_daily_total c where c.proj_name='"+item[0]+"' group by c.proj_name "       
                    sql_get_totalactive = "select c.date_s,sum(c.total_num) from table_activate_num_daily_total c  group by c.date_s  order  by c.date_s desc"                          

                cur,conn = get_pgconn()
                #sql_get_act = "select proj_name,date_s,act_num from table_activate_num where proj_id=" + str(proj_id)+" and date_s>='"+date_from+"' and date_s<='" +date_to+ "' order by date_s desc"
                cur.execute(sql_get_totalactive)
                #print sql_get_totalactive
                results_get_totalactive = cur.fetchall()
                close_pgconn(cur,conn)  

                print sql_get_totalactive

                if results_get_totalactive!=[]:
                    each_result['total_active'] = results_get_totalactive[0][1]
                else:
                    each_result['total_active'] = 0

                # ######get total duli begin
                # if results_get_type[0][0]=='客户' or results_get_type[0][0]=='商务':
                #     # group by date
                #     # sql_get_totalduli_ids = "select c.proj_name,count(c.id) from table_proj b  join table_activate_num_ids c on b.proj_name=c.proj_name  where b.proj_id in "+proj_id_col+" and c.proj_name='"+item[0]+"' group by c.proj_name"        
                #     sql_get_totalduli_ids = "select c.date_s,count(c.id) from table_proj b  join table_activate_num_ids c on b.proj_name=c.proj_name  where b.proj_id in "+proj_id_col+"  group by c.date_s order by c.date_s desc"                    
                # else:
                #     # group by date
                #     # sql_get_totalduli_ids = "select c.proj_name,count(c.id) from table_activate_num_ids c  where c.proj_name='"+item[0]+"' group by c.proj_name"       
                #     sql_get_totalduli_ids = "select c.date_s,count(c.id) from table_activate_num_ids c   group by c.date_s order by c.date_s desc"                          
                # cur,conn = get_pgconn()
                # cur.execute(sql_get_totalduli_ids)
                # results_get_totalduli_ids = cur.fetchall()
                # close_pgconn(cur,conn)  

                # if results_get_totalduli_ids!=[]:
                #     each_result['total_duli'] = results_get_totalduli_ids[0][1]
                # else:
                #     each_result['total_duli'] = 0

                # ######get total duli over

                ######get total duli begin
                if results_get_dailyactive!=[]:
                    if results_get_type[0][0]=='客户' or results_get_type[0][0]=='商务':
                        # group by date
                        # sql_get_totalduli_ids = "select c.proj_name,count(c.id) from table_proj b  join table_activate_num_ids c on b.proj_name=c.proj_name  where b.proj_id in "+proj_id_col+" and c.proj_name='"+item[0]+"' group by c.proj_name"                 
                        sql_get_totalduli_ids = "select count(c.id) from table_proj b  join table_activate_num_ids c on b.proj_name=c.proj_name  where c.date_s<='" +str(results_get_dailyactive[0][0])+"'"
                    else:
                        # group by date
                        # sql_get_totalduli_ids = "select c.proj_name,count(c.id) from table_activate_num_ids c  where c.proj_name='"+item[0]+"' group by c.proj_name"  
                        sql_get_totalduli_ids = "select count(c.id) from table_activate_num_ids c  where c.date_s<='" +str(results_get_dailyactive[0][0])+"'"
                        
                    cur,conn = get_pgconn()
                    cur.execute(sql_get_totalduli_ids)
                    results_get_totalduli_ids = cur.fetchall()
                    close_pgconn(cur,conn)  

                    if results_get_totalduli_ids!=[]:
                        total_duli_s = results_get_totalduli_ids[0][0]
                    else:
                        total_duli_s = 0

                ######get total duli over                

                # now_total_duli = total_duli_s - item[1]

                if results_get_dailyactive!=[]:
                    result_str = result_str+'{"proj_name":"' + each_result['proj_name'] +'",'+'"daily_active":"' + str(each_result['active']) + '","duli":"' + str(each_result['duli']) +'",' + '"total_active":"'+str(each_result['total_active']) + '","total_duli":"'+ str(total_duli_s)+'","date":"'+str(results_get_dailyactive[0][0])+'","sub_channel_name":"'+"Tripics"+'"},'

    result_str = result_str[0:int(len(result_str))-1]    
    result_str = '{"allData":[' + result_str +']}'        
    #print result_item
    #return HttpResponse("<p>"+str(result_item)+"</p>")
    #print result_str
    return result_str  

#interface to get tongji data to frontpage
def get_tongji_to_frontpage_proj(user_name,date_1,date_2,proj):

    # print date_1
    # print date_2
    #print date_range
    print "555555555555555555555"
    # cur,conn = get_pgconn()
    # sql_get_pid = "select proj_id from table_proj where proj_name='"+proj+"'"
    # cur.execute(sql_get_pid)
    # results_get_pid = cur.fetchall()
    # close_pgconn(cur,conn) 

    # proj_id_p = str(results_get_pid[0][0])

    date_range_array=[]
    date_range_array.append(date_1)
    date_range_array.append(date_2)
    date_range_box = []
    date_from = ""
    date_to = ""

    fil = False

    if date_1!="undefined" and date_1!="" and date_2!="undefined" and date_2!="" and date_1!="first" and date_2!="first":
        fil = True
        for j in date_range_array:
            date_array = j.split(' ')
            month = date_array[1]
            day = date_array[2]
            year = date_array[3]
            if month == 'Jan':
                month = '01'
            elif month == 'Feb':
                month = '02' 
            elif month == 'Mar':
                month = '03' 
            elif month == 'Apr':
                month = '04'             
            elif month == 'May':
                month = '05'     
            elif month == 'Jun':
                month = '06' 
            elif month == 'Jul':
                month = '07' 
            elif month == 'Aug':
                month = '08'             
            elif month == 'Sep':
                month = '09'   
            elif month == 'Oct':
                month = '10' 
            elif month == 'Nov':
                month = '11'             
            elif month == 'Dec':
                month = '12' 
            formatted_date = year +"-"+ month +"-"+ day
            date_range_box.append(formatted_date)

        date_from = date_range_box[0]
        date_to = date_range_box[1]
    else:
        now = datetime.datetime.now()
        one_week_ago = now - datetime.timedelta(days=7)
        date_str = now.strftime('%Y-%m-%d') 
        date_str_one_week_ago = one_week_ago.strftime('%Y-%m-%d')  
        date_from = date_str_one_week_ago
        date_to = date_str

    # print date_from
    # print date_to

    cur,conn = get_pgconn()
    sql_get_type = "select user_type ,related_projs from table_user where user_name='"+user_name+"'"
    cur.execute(sql_get_type)
    results_get_type = cur.fetchall()
    close_pgconn(cur,conn) 

    # print "fdddd"
    # print str(results_get_type[0][1])

    if str(results_get_type[0][1])!="None":
        proj_id_col = "("+results_get_type[0][1]+")"
    else:
        proj_id_col = "nothing"

    # ######get total duli begin
    # if results_get_type[0][0]=='客户' or results_get_type[0][0]=='商务':
    #     # group by date
    #     # sql_get_totalduli_ids = "select c.proj_name,count(c.id) from table_proj b  join table_activate_num_ids c on b.proj_name=c.proj_name  where b.proj_id in "+proj_id_col+" and c.proj_name='"+item[0]+"' group by c.proj_name"                 
    #     sql_get_totalduli_ids = "select count(c.id) from table_proj b  join table_activate_num_ids c on b.proj_name=c.proj_name  where c.date_s<='" +date_to+"'"
    # else:
    #     # group by date
    #     # sql_get_totalduli_ids = "select c.proj_name,count(c.id) from table_activate_num_ids c  where c.proj_name='"+item[0]+"' group by c.proj_name"  
    #     sql_get_totalduli_ids = "select count(c.id) from table_activate_num_ids c  where c.date_s<='" +date_to+"'"
        
    # cur,conn = get_pgconn()
    # cur.execute(sql_get_totalduli_ids)
    # results_get_totalduli_ids = cur.fetchall()
    # close_pgconn(cur,conn)  

    # if results_get_totalduli_ids!=[]:
    #     total_duli_s = results_get_totalduli_ids[0][0]
    # else:
    #     total_duli_s = 0

    # ######get total duli over

    if results_get_type[0][0]=='客户' or results_get_type[0][0]=='商务':
        # group by date 
        # sql_get_duli_ids = "select c.proj_name,count(c.id) from table_proj b  join table_activate_num_ids c on b.proj_name=c.proj_name  where b.proj_id in "+proj_id_col+" and c.date_s>='"+date_from+"' and c.date_s<='" +date_to+ "' group by c.proj_name"
        sql_get_duli_ids = "select c.date_s,count(c.id)  from table_proj b  join table_activate_num_ids c on b.proj_name=c.proj_name  where b.proj_id in "+proj_id_col+" and c.date_s>='"+date_from+"' and c.date_s<='" +date_to+ "' "+"and c.sub_channel_name='"+proj+"' group by c.date_s order  by c.date_s desc"
 
    else:
        # group by date
        # sql_get_duli_ids = "select c.proj_name,count(c.id) from table_activate_num_ids c  where c.date_s>='"+date_from+"' and c.date_s<='" +date_to+ "' group by c.proj_name"
        sql_get_duli_ids = "select c.date_s,count(c.id)   from table_activate_num_ids c  where c.date_s>='"+date_from+"' and c.date_s<='" +date_to+ "'"+"  and c.sub_channel_name='"+proj+"' "+" group by c.date_s order by c.date_s desc"

    cur,conn = get_pgconn()
    #sql_get_act = "select proj_name,date_s,act_num from table_activate_num where proj_id=" + str(proj_id)+" and date_s>='"+date_from+"' and date_s<='" +date_to+ "' order by date_s desc"
    cur.execute(sql_get_duli_ids)
    # print sql_get_duli_ids
    results_get_duli_ids = cur.fetchall()
    close_pgconn(cur,conn)        

    result_item = []
    result_str = ""
    
    if results_get_duli_ids!=[]:
        for index,item in enumerate(results_get_duli_ids):

            if results_get_type[0][0]=='客户' or results_get_type[0][0]=='商务':
                # group by date
                # sql_get_dailyactive = "select c.proj_name,sum(c.total_num) from table_proj b  join table_activate_num_daily_total c on b.proj_name=c.proj_name  where b.proj_id in "+proj_id_col+" and c.date_s>='"+date_from+"' and c.date_s<='" +date_to+"' and c.proj_name='"+item[0]+ "' group by c.proj_name"                
                sql_get_dailyactive = "select c.date_s,sum(c.total_num) from table_proj b  join table_activate_num_daily_total c on b.proj_name=c.proj_name  where c.date_s='"+item[0]+"' and b.proj_id in "+proj_id_col+" and c.date_s>='"+date_from+"' and c.date_s<='" +date_to+"' and c.sub_channel_name='"+proj+"'"+"  group by c.date_s order  by c.date_s desc"
            else:
                # group by date
                # sql_get_dailyactive = "select c.proj_name,sum(c.total_num) from table_activate_num_daily_total c where c.date_s>='"+date_from+"' and c.date_s<='" +date_to+"' and c.proj_name='"+item[0]+"' group by c.proj_name "                
                sql_get_dailyactive = "select c.date_s,sum(c.total_num) from table_activate_num_daily_total c where  c.date_s='"+item[0]+"' and  c.date_s>='"+date_from+"' and c.date_s<='" +date_to+"' and c.sub_channel_name='"+proj+"'"+"  group by c.date_s  order  by c.date_s desc"

            cur,conn = get_pgconn()
            #sql_get_act = "select proj_name,date_s,act_num from table_activate_num where proj_id=" + str(proj_id)+" and date_s>='"+date_from+"' and date_s<='" +date_to+ "' order by date_s desc"
            cur.execute(sql_get_dailyactive)
            #print sql_get_dailyactive
            results_get_dailyactive = cur.fetchall()
            close_pgconn(cur,conn)    


            each_result = {}
            # group by date
            # each_result['proj_name'] = item[0]
            each_result['proj_name'] = "Tripics"
            if results_get_dailyactive!=[]:
                each_result['active'] = results_get_dailyactive[0][1]
            else:
                each_result['active'] = 0
            #print each_result['title']
            #print type(each_result['title'])       
            each_result['duli'] = item[1]   
            #each_result['rate'] = item[2] 
            #result_str_each = each_result['title'] + "," + each_result['number']
            result_item.append(each_result)

            #each_result['lively_num'] = int(results[0][0]*each_result['rate'])      
            if results_get_type[0][0]=='客户' or results_get_type[0][0]=='商务':
                # group by date
                # sql_get_totalactive = "select c.proj_name,sum(c.total_num) from table_proj b  join table_activate_num_daily_total c on b.proj_name=c.proj_name  where b.proj_id in "+proj_id_col+" and c.proj_name='"+item[0]+ "' group by c.proj_name"
                sql_get_totalactive = "select c.date_s,sum(c.total_num) from table_proj b  join table_activate_num_daily_total c on b.proj_name=c.proj_name  where b.proj_id in "+proj_id_col+" and c.sub_channel_name='"+proj+"'"+"  group by c.date_s order  by c.date_s desc"                
            else:
                # group by date
                # sql_get_totalactive = "select c.proj_name,sum(c.total_num) from table_activate_num_daily_total c where c.proj_name='"+item[0]+"' group by c.proj_name "                
                sql_get_totalactive = "select c.date_s,sum(c.total_num) from table_activate_num_daily_total c where c.sub_channel_name='"+proj+"'"+"group by c.date_s  order  by c.date_s desc"            

            cur,conn = get_pgconn()
            #sql_get_act = "select proj_name,date_s,act_num from table_activate_num where proj_id=" + str(proj_id)+" and date_s>='"+date_from+"' and date_s<='" +date_to+ "' order by date_s desc"
            cur.execute(sql_get_totalactive)
            #print sql_get_totalactive
            results_get_totalactive = cur.fetchall()
            close_pgconn(cur,conn)  

            each_result['total_active'] = results_get_totalactive[0][1]

            ######get total duli begin
            if results_get_type[0][0]=='客户' or results_get_type[0][0]=='商务':
                # group by date
                # sql_get_totalduli_ids = "select c.proj_name,count(c.id) from table_proj b  join table_activate_num_ids c on b.proj_name=c.proj_name  where b.proj_id in "+proj_id_col+" and c.proj_name='"+item[0]+"' group by c.proj_name"                 
                sql_get_totalduli_ids = "select count(c.id) from table_proj b  join table_activate_num_ids c on b.proj_name=c.proj_name  where c.date_s<='" +str(item[0])+"'"+" and c.sub_channel_name='"+sub_channel_name+"'"
            else:
                # group by date
                # sql_get_totalduli_ids = "select c.proj_name,count(c.id) from table_activate_num_ids c  where c.proj_name='"+item[0]+"' group by c.proj_name"  
                sql_get_totalduli_ids = "select count(c.id) from table_activate_num_ids c  where c.date_s<='" +str(item[0])+"'"+" and c.sub_channel_name='"+proj+"'"
                
            cur,conn = get_pgconn()
            cur.execute(sql_get_totalduli_ids)
            results_get_totalduli_ids = cur.fetchall()
            close_pgconn(cur,conn)  

            if results_get_totalduli_ids!=[]:
                total_duli_s = results_get_totalduli_ids[0][0]
            else:
                total_duli_s = 0

            ######get total duli over

            result_str = result_str+'{"proj_name":"' + each_result['proj_name'] +'",'+'"daily_active":"' + str(each_result['active']) + '","duli":"' + str(each_result['duli']) +'",' + '"total_active":"'+str(each_result['total_active']) + '","total_duli":"'+ str(total_duli_s) +'","date":"'+str(item[0])+'","sub_channel_name":"'+proj+'"},'
    else:
        if results_get_type[0][0]=='客户' or results_get_type[0][0]=='商务':
            sql_get_today_none = "select b.proj_name from table_proj b where b.proj_id in "+proj_id_col
        else:
            sql_get_today_none = "select b.proj_name from table_proj b"

        cur,conn = get_pgconn()
        cur.execute(sql_get_today_none)
        results_get_today_none = cur.fetchall()
        close_pgconn(cur,conn)        

        if results_get_today_none!=[]:
            for item in results_get_today_none:            
                if results_get_type[0][0]=='客户' or results_get_type[0][0]=='商务':
                    # group by date
                    # sql_get_dailyactive = "select c.proj_name,sum(c.total_num) from table_proj b  join table_activate_num_daily_total c on b.proj_name=c.proj_name  where b.proj_id in "+proj_id_col+" and c.date_s>='"+date_from+"' and c.date_s<='" +date_to+"' and c.proj_name='"+item[0]+ "' group by c.proj_name"
                    sql_get_dailyactive = "select c.date_s,sum(c.total_num) from table_proj b  join table_activate_num_daily_total c on b.proj_name=c.proj_name  where  c.date_s='"+item[0]+"' and b.proj_id in "+proj_id_col+" and c.date_s>='"+date_from+"' and c.date_s<='" +date_to+"' and c.sub_channel_name='"+proj+"'"+" group by c.date_s order  by c.date_s desc"                    
                else:
                    # group by date
                    # sql_get_dailyactive = "select c.proj_name,sum(c.total_num) from table_activate_num_daily_total c where c.date_s>='"+date_from+"' and c.date_s<='" +date_to+"' and c.proj_name='"+item[0]+"' group by c.proj_name "    
                    sql_get_dailyactive = "select c.date_s,sum(c.total_num) from table_activate_num_daily_total c where c.date_s='"+item[0]+"' and  c.date_s>='"+date_from+"' and c.date_s<='" +date_to+"' and c.sub_channel_name='"+proj+"'"+"  group by c.date_s  order  by c.date_s desc"                             

                cur,conn = get_pgconn()
                #sql_get_act = "select proj_name,date_s,act_num from table_activate_num where proj_id=" + str(proj_id)+" and date_s>='"+date_from+"' and date_s<='" +date_to+ "' order by date_s desc"
                cur.execute(sql_get_dailyactive)
                #print sql_get_dailyactive
                results_get_dailyactive = cur.fetchall()
                close_pgconn(cur,conn)    


                each_result = {}
                # group by date
                # each_result['proj_name'] = item[0]
                each_result['proj_name'] = "Tripics"
                if results_get_dailyactive!=[]:
                    each_result['active'] = results_get_dailyactive[0][1]
                else:
                    each_result['active'] = 0
                #print each_result['title']
                #print type(each_result['title'])       
                each_result['duli'] = 0   
                #each_result['rate'] = item[2] 
                #result_str_each = each_result['title'] + "," + each_result['number']
                result_item.append(each_result)

                #each_result['lively_num'] = int(results[0][0]*each_result['rate'])      

                if results_get_type[0][0]=='客户' or results_get_type[0][0]=='商务':
                    # group by date
                    # sql_get_totalactive = "select c.proj_name,sum(c.total_num) from table_proj b  join table_activate_num_daily_total c on b.proj_name=c.proj_name  where b.proj_id in "+proj_id_col+" and c.proj_name='"+item[0]+ "' group by c.proj_name"
                    sql_get_totalactive = "select c.date_s,sum(c.total_num) from table_proj b  join table_activate_num_daily_total c on b.proj_name=c.proj_name  where b.proj_id in "+proj_id_col+"' and c.sub_channel_name='"+proj+"'"+"  group by c.date_s order by c.date_s desc"                    
                else:
                    # group by date
                    # sql_get_totalactive = "select c.proj_name,sum(c.total_num) from table_activate_num_daily_total c where c.proj_name='"+item[0]+"' group by c.proj_name "       
                    sql_get_totalactive = "select c.date_s,sum(c.total_num) from table_activate_num_daily_total c where c.sub_channel_name='"+proj+"'"+"  group by c.date_s  order  by c.date_s desc"                          

                cur,conn = get_pgconn()
                #sql_get_act = "select proj_name,date_s,act_num from table_activate_num where proj_id=" + str(proj_id)+" and date_s>='"+date_from+"' and date_s<='" +date_to+ "' order by date_s desc"
                cur.execute(sql_get_totalactive)
                #print sql_get_totalactive
                results_get_totalactive = cur.fetchall()
                close_pgconn(cur,conn)  

                print sql_get_totalactive

                if results_get_totalactive!=[]:
                    each_result['total_active'] = results_get_totalactive[0][1]
                else:
                    each_result['total_active'] = 0

                # ######get total duli begin
                # if results_get_type[0][0]=='客户' or results_get_type[0][0]=='商务':
                #     # group by date
                #     # sql_get_totalduli_ids = "select c.proj_name,count(c.id) from table_proj b  join table_activate_num_ids c on b.proj_name=c.proj_name  where b.proj_id in "+proj_id_col+" and c.proj_name='"+item[0]+"' group by c.proj_name"        
                #     sql_get_totalduli_ids = "select c.date_s,count(c.id) from table_proj b  join table_activate_num_ids c on b.proj_name=c.proj_name  where b.proj_id in "+proj_id_col+"  group by c.date_s order by c.date_s desc"                    
                # else:
                #     # group by date
                #     # sql_get_totalduli_ids = "select c.proj_name,count(c.id) from table_activate_num_ids c  where c.proj_name='"+item[0]+"' group by c.proj_name"       
                #     sql_get_totalduli_ids = "select c.date_s,count(c.id) from table_activate_num_ids c   group by c.date_s order by c.date_s desc"                          
                # cur,conn = get_pgconn()
                # cur.execute(sql_get_totalduli_ids)
                # results_get_totalduli_ids = cur.fetchall()
                # close_pgconn(cur,conn)  

                # if results_get_totalduli_ids!=[]:
                #     each_result['total_duli'] = results_get_totalduli_ids[0][1]
                # else:
                #     each_result['total_duli'] = 0

                # ######get total duli over

                ######get total duli begin
                if results_get_dailyactive!=[]:
                    if results_get_type[0][0]=='客户' or results_get_type[0][0]=='商务':
                        # group by date
                        # sql_get_totalduli_ids = "select c.proj_name,count(c.id) from table_proj b  join table_activate_num_ids c on b.proj_name=c.proj_name  where b.proj_id in "+proj_id_col+" and c.proj_name='"+item[0]+"' group by c.proj_name"                 
                        sql_get_totalduli_ids = "select count(c.id) from table_proj b  join table_activate_num_ids c on b.proj_name=c.proj_name  where c.date_s<='" +str(results_get_dailyactive[0][0])+"'"+" and c.sub_channel_name='"+proj+"'"
                    else:
                        # group by date
                        # sql_get_totalduli_ids = "select c.proj_name,count(c.id) from table_activate_num_ids c  where c.proj_name='"+item[0]+"' group by c.proj_name"  
                        sql_get_totalduli_ids = "select count(c.id) from table_activate_num_ids c  where c.date_s<='" +str(results_get_dailyactive[0][0])+"'"+" and c.sub_channel_name='"+proj+"'"
                        
                    cur,conn = get_pgconn()
                    cur.execute(sql_get_totalduli_ids)
                    results_get_totalduli_ids = cur.fetchall()
                    close_pgconn(cur,conn)  

                    if results_get_totalduli_ids!=[]:
                        total_duli_s = results_get_totalduli_ids[0][0]
                    else:
                        total_duli_s = 0

                ######get total duli over                

                # now_total_duli = total_duli_s - item[1]

                if results_get_dailyactive!=[]:
                    result_str = result_str+'{"proj_name":"' + each_result['proj_name'] +'",'+'"daily_active":"' + str(each_result['active']) + '","duli":"' + str(each_result['duli']) +'",' + '"total_active":"'+str(each_result['total_active']) + '","total_duli":"'+ str(total_duli_s)+'","date":"'+str(results_get_dailyactive[0][0])+'","sub_channel_name":"'+proj+'"},'

    result_str = result_str[0:int(len(result_str))-1]    
    result_str = '{"allData":[' + result_str +']}'        
    #print result_item
    #return HttpResponse("<p>"+str(result_item)+"</p>")
    #print result_str
    return result_str  

#insert subchannel into db
def insert_subchannel_into_db():

    # sql = "select android_id, imsi, imei, wifi_mac"
    # cur,conn = get_pgconn()
    # cur.execute(sql_get_totalduli_ids)
    # results_get_ids = cur.fetchall()
    # close_pgconn(cur,conn)

    time = ""
    time_p = ""
    daily_table_last = ""

    sql_get_tables = "select pg_tables.tablename from pg_tables order by pg_tables.tablename"
    cur,conn= get_pgconn()
    cur.execute(sql_get_tables)
    results_get_tables = cur.fetchall()
    close_pgconn(cur,conn)

    daily_table_list = []
    for item_tables in results_get_tables:
        daily_table_list.append(item_tables[0])

    f_name_tar = "/home/charles/log/kkk"

    ############ 2016 passed end
    for file in os.listdir(f_name_tar + "_files/"):
        f = open(f_name_tar + "_files/"+file)
        ############ 2016 passed start
        print file

        if file.count('production_')==0:
            print "Not log file !!!!!"
            # os.remove(f_name_tar + "_files/"+file)
            continue
        ############ 2016 passed end

        #f = open(file)

        inde_ad = 0

        for i in f:
            i = i.encode('utf-8')
            #print i
            if i.count('sub_channel')==0:
                # ############ 2016 passed start
                # if i.count(']  INFO -- : [')!=0:
                #     time = i[4:14]
                #     time_p = time.replace("-","_")
                # ############ 2016 passed end
                continue
            else:
                ind_imsi = i.find('imsi')
                ind_sub_channel = i.find('sub_channel')
                ind_sub_channel_id = i.find('sub_channel_id')
                ind_mac = i.find('mac_addr')

                if ind_imsi==-1 or ind_mac==-1:
                    continue
                else:
                    imsi = i[ind_imsi+7:ind_imsi+22]

                    sub_channel_clip = i[ind_sub_channel:-1]
                    #print sub_channel_clip
                    first_get_yinhao = str(sub_channel_clip).find('"')
                    again_get_yinhao = sub_channel_clip.find('"',14)
                    #print first_get_yinhao
                    #print again_get_yinhao

                    sub_channel_name = sub_channel_clip[first_get_yinhao+1:again_get_yinhao]

                    sub_channel_id_clip = i[ind_sub_channel_id:-1]
                    # first_get_yinhao_id = sub_channel_id_clip.find['"']
                    again_get_yinhao_id = sub_channel_id_clip.find(',',17)
                    sub_channel_id = sub_channel_id_clip[16:again_get_yinhao_id]

                    wifi_mac = i[ind_mac+11:ind_mac+28]

                    #print sub_channel_id_clip
                    #print sub_channel_id
                    #print sub_channel_name

                    #info_join = imsi+"$&&&#####"+imei+"$&&&#####"+android_id+"$&&&#####"+wifi_mac

                    sql_get_t = "select id from table_activate_num_ids  where wifi_mac='"+wifi_mac+"' and sub_channel_name is NULL" 
                    cur,conn= get_pgconn()
                    cur.execute(sql_get_t)
                    results_get_t = cur.fetchall()
                    close_pgconn(cur,conn)

                    if results_get_t==[]:
                       continue

                    # if results_get_t[0][0]!="":
                    #    #print "updated , skipping !!!"
                    #    #print results_get_t[0][0]
                    #    #print str(results_get_t[0][0])
                    #    continue


                    ### calculating independent users
                    cur,conn= get_pgconn()
                    sql_update_sub_channel = "update table_activate_num_ids set sub_channel_name='"+sub_channel_name+"',sub_channel_id='" +sub_channel_id + "' where wifi_mac='"+wifi_mac+"'"
                    cur.execute(sql_update_sub_channel)
                    commit_conn(conn)
                    close_pgconn(cur,conn)


                    ### calculating daily active users

                    now_t = datetime.datetime.now()
                    now_str_t = now_t.strftime('%Y_%m_%d')
                    daily_table = "table_daily_active_"+now_str_t

                    ############ 2016 passed start
                    daily_table = "table_daily_active_"+time_p
                    #daily_table_last = daily_table
                    if daily_table in daily_table_list:
                        print "daily table existed !!!!!"
                    else:
                        create_new_table_for_daily_active_pass(time_p)
                        daily_table_last = daily_table
                        daily_table_list.append(daily_table)
                    ############ 2016 passed end
                    cur,conn= get_pgconn()
                    sql_update_sub_channel = "update "+daily_table+" set sub_channel_name='"+sub_channel_name+"',sub_channel_id='" +sub_channel_id + "' where wifi_mac='"+wifi_mac+"'"
                    cur.execute(sql_update_sub_channel)
                    commit_conn(conn)
                    close_pgconn(cur,conn)

                    inde_ad = inde_ad + 1
                    print("duli id cals num : "+str(inde_ad))


        f.close()
        # os.remove(f_name_tar + "_files/"+file)

    #os.remove(file_name)
    #os.remove(f_name_tar)
    #shutil.rmtree(f_name_tar + "_files/")

    print daily_table_list

    return "OK"

#adding columns to duli
def add_columns_to_duli_tables():
    
    sql_add_column ="alter table table_activate_num_ids add sub_channel_name text, add sub_channel_id text" 
    print sql_add_column
    cur,conn= get_pgconn()
    cur.execute(sql_add_column)
    commit_conn(conn)   
    close_pgconn(cur,conn) 

    return "OK"

def add_columns_to_total_tables():
    
    sql_add_column ="alter table table_activate_num_daily_total add sub_channel_name text, add sub_channel_id text" 
    print sql_add_column
    cur,conn= get_pgconn()
    cur.execute(sql_add_column)
    commit_conn(conn)   
    close_pgconn(cur,conn) 

    return "OK"    

#adding columns to daily active tables
def add_columns_to_dailyactive_tables():
    
    sql_get_tables = "select pg_tables.tablename from pg_tables  where pg_tables.tablename like 'table_daily_active_%' order by pg_tables.tablename"
    cur,conn= get_pgconn()
    cur.execute(sql_get_tables)
    results_get_tables = cur.fetchall()
    close_pgconn(cur,conn) 

    for item in results_get_tables:
        sql_add_column ="alter table " + item[0] + " add sub_channel_name text, add sub_channel_id text" 
        print sql_add_column
        cur,conn= get_pgconn()
        cur.execute(sql_add_column)
        commit_conn(conn)   
        close_pgconn(cur,conn) 

    return "OK"

#insert daily active num for frontpage display
def insert_manual_daily_active(proj_id, num):
    return "OK"

#for testing logfile
def insert_formatted_data_to_db_imsi():
    f = open('/home/charles/production_2016-11-28.log.3', 'r')

    iii = 0
    for i in f:
        print iii
        iii+=1
        #if i.count('imsi')==0:
        #if i.count('android_id')==0:
        if i.count('imei')==0:
            print "nononnonononononono"
            continue
        else:
            print "yesyesyesyesyesyesyes"
            ind_imsi = i.index('imei')
            #ind_imsi = i.index('imsi')
            #ind_imsi = i.index('android_id')
            imsi = i[ind_imsi+7:ind_imsi+22]
            #imsi = i[ind_imsi+13:ind_imsi+28]
            print imsi
            if judge_imsi_exsit(imsi)==False:
                print "not exsited!!!!!!!!!!!!!!!!!!!!!!!!!"
                #f_w = open('/home/charles/myImsi.txt','a')
                #f_w = open('/home/charles/myAnID.txt','a')
                f_w = open('/home/charles/myImei.txt','a')
                imsi_com = imsi+"\n"
                f_w.write(imsi_com)
                #f_w.write('\n')
                f_w.close()
            else:
                continue

    return "OK"    

#for testing logfile
def judge_imsi_exsit(imsi):
    print "exsitance judging!!!!!!"
    print imsi

    #f = open('/home/charles/myImsi.txt', 'r')
    #f = open('/home/charles/myAnID.txt', 'r')
    f = open('/home/charles/myImei.txt', 'r')

    for i in f:
        print i
        if i.count(imsi)>0:
            print "fffdfddfd"
            return True
        else:
            continue

    f.close()
    return False    

def check_files_for_updated():

    f_name_tar = "/home/charles/log/kkk" 

    ############ 2016 passed end 
    for file in os.listdir(f_name_tar + "_files/"):
        f = open(f_name_tar + "_files/"+file)
        ############ 2016 passed start
        #print file
        ############ 2016 passed end

        #f = open(file)

        inde_ad = 0

        for index,i in enumerate(f):
            imsi_col = ['2300150073625550','2550142704699680','4660560025530690']

            for each in imsi_col:
                if i.count(each)>0:
                    print "imsi "+str(each)+" found !!! file name : "+file+" line num : "+str(index+1)

        f.close()
        # os.remove(f_name_tar + "_files/"+file)

    #os.remove(file_name)
    #os.remove(f_name_tar)
    #shutil.rmtree(f_name_tar + "_files/")

    ##print daily_table_list

    return "OK"