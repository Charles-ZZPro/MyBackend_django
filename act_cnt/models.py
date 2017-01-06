#-*-coding:utf-8-*-
from __future__ import unicode_literals

from django.db import models
import psycopg2
import sys
import datetime
import random

reload(sys)
sys.setdefaultencoding('utf-8')

# Create your models here.
def get_pgconn():
	# Connect to an existing database
	conn = psycopg2.connect("dbname=myTestDB user=postgres password=postgres")
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
    sql_get_act = "select proj_name, proj_id, sum(act_num) cnt_num from table_activate_num_fake group by proj_id, proj_name order by proj_id "
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
    rand1 = random.randint(21000,23000)

    t_str_end = '2017-01-08'

    t_str_end_fake = datetime.datetime.strptime(t_str_end,'%Y-%m-%d')

    while now_fake.strftime('%Y-%m-%d') < t_str_end_fake.strftime('%Y-%m-%d'):
        now_fake=now_fake+delta

        date_str = now_fake.strftime('%Y-%m-%d')
        #rand1 = random.randint(30,100)
        
        rand1 = rand1 + random.randint(1200, 1800)
        #rand1 = rand1 + random.randint(20, 30)
        
        #rand3 = str(random.randint(1000, 1000000))
        #rand4 = str(random.randint(1000, 1000000))

        date_str = now_fake.strftime('%Y-%m-%d')  

        cur,conn = get_pgconn()
        # cur.execute("insert into table_activate_num(proj_name,date_s,act_num,proj_id) values(%s,%s,%s,%s)",('第一个项目',date_str,rand1,1))
        # conn.commit()
        # cur.execute("insert into table_activate_num(proj_name,date_s,act_num,proj_id) values(%s,%s,%s,%s)",('第二个项目',date_str,rand2,2))    
        # cur.execute("insert into table_activate_num(proj_name,date_s,act_num,proj_id) values(%s,%s,%s,%s)",('第三个项目',date_str,rand3,3))
        # cur.execute("insert into table_activate_num(proj_name,date_s,act_num,proj_id) values(%s,%s,%s,%s)",('第四个test项目',date_str,rand4,4))        
        sql_insert_act = "insert into table_activate_num_fake(proj_name,date_s,act_num,proj_id,country) values('project_1','"+date_str+"',"+str(rand1)+",1,'India');"

        #print sql_insert_act                    
        cur.execute(sql_insert_act)
        commit_conn(conn)   
        close_pgconn(cur,conn)

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