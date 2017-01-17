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
    sql_get_act = "select user_name, passwd from table_user"
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
        join_user = join_user + each_result['user_name'] + each_result['passwd'] + "Mypassinstringhere"
 
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
      'CONSTRAINT '+daily_table+'_pkey PRIMARY KEY (id))'\
      'WITH (OIDS=FALSE);'\
      'ALTER TABLE public.'+daily_table+' OWNER TO "littleAdmin";'
    cur.execute(sql_create)
    commit_conn(conn)   
    close_pgconn(cur,conn) 

    return "OK"


#从rawdata压缩文件中提取有效新增独立用户，插入数据库
def insert_formatted_data_to_db(file_name,time,proj_name):

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
                sql_get_all = "select count(id) from table_activate_num_ids  where imsi='" + imsi + "' or imei='" + imei +"' or android_id='"+android_id+"' or wifi_mac='"+wifi_mac+"' and proj_name='"+proj_name+"'"
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
                sql_get_all = "select count(id) from "+daily_table+"  where imsi='" + imsi + "' or imei='" + imei +"' or android_id='"+android_id+"' or wifi_mac='"+wifi_mac+"' and proj_name='"+proj_name+"'"
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
    os.remove(f_name_tar)
    shutil.rmtree(f_name_tar + "_files/")

    return "OK"

#insert daily total count for every project to database
def insert_all_daily_data():
    now_t = datetime.datetime.now()
    now_str_t = now_t.strftime('%Y_%m_%d')
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