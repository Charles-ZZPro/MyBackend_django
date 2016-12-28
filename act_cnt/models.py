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
    sql_get_act = "select proj_name, proj_id, sum(act_num) cnt_num from table_activate_num group by proj_id, proj_name order by proj_id "
    cur.execute(sql_get_act)
    results = cur.fetchall()
    close_pgconn(cur,conn)
    result_item = []
    result_str = ""
    
    for item in results:
    	each_result = {}
    	each_result['title'] = item[0]
    	each_result['title'] = each_result['title'].encode('utf-8')
    	print type(each_result['title'])    	
    	#print each_result['title']
    	each_result['number'] = str(item[2])
        #result_str_each = each_result['title'] + "," + each_result['number']
        result_item.append(each_result)
        result_str = result_str+'{"title":"' + each_result['title'] +'",'+'"number":"' + each_result['number'] + '","id":"'+str(item[1])+'"},'
    #print result_item
    #return HttpResponse("<p>"+str(result_item)+"</p>")
    result_str = result_str[0:int(len(result_str))-1]    
    result_str = '{"tuple":[' + result_str +']}'
    print result_str
    #result_str = result_str.replace("\","")
    #print result_str
    json_total = {}
    json_total['tuple'] = result_item

    #return json_total
    return result_str

def get_active_dailynums(proj_id):
    cur,conn = get_pgconn()
    sql_get_act = "select proj_name,date_s,act_num from table_activate_num where proj_id=" + str(proj_id)+" order by date_s desc"
    cur.execute(sql_get_act)
    results = cur.fetchall()
    close_pgconn(cur,conn)    
    result_item = []
    result_str = ""
    
    for item in results:
    	each_result = {}
    	each_result['date'] = item[1]
    	each_result['date'] = each_result['date'].encode('utf-8')
    	#print each_result['title']
    	#print type(each_result['title'])    	
    	each_result['number'] = int(item[2])	
        #result_str_each = each_result['title'] + "," + each_result['number']
        result_item.append(each_result)

        cur,conn = get_pgconn()
        sql_get_act_each_total = "select sum(act_num) from table_activate_num where proj_id=" + str(proj_id)+" and date_s<='" + each_result['date'] +"'"
        cur.execute(sql_get_act_each_total)
        results = cur.fetchall()       
        close_pgconn(cur,conn)        

        result_str = result_str+'{"date":"' + each_result['date'] +'",'+'"dayNumber":"' + str(each_result['number']) + '","totalNumber":"' + str(results[0][0]) +'"},'

    result_str = result_str[0:int(len(result_str))-1]    
    result_str = '{"tuple":[' + result_str +']}'        
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
    sql_get_act = "select proj_name,date_s,act_num from table_activate_num where proj_id=" + str(proj_id)+" and date_s>='"+date_from+"' and date_s<='" +date_to+ "' order by date_s desc"
    cur.execute(sql_get_act)
    results = cur.fetchall()
    close_pgconn(cur,conn)    
    result_item = []
    result_str = ""
    
    if results!=[]:
        for item in results:
            each_result = {}
            each_result['date'] = item[1]
            each_result['date'] = each_result['date'].encode('utf-8')
            #print each_result['title']
            #print type(each_result['title'])       
            each_result['number'] = int(item[2])    
            #result_str_each = each_result['title'] + "," + each_result['number']
            result_item.append(each_result)

            cur,conn = get_pgconn()
            sql_get_act_each_total = "select sum(act_num) from table_activate_num where proj_id=" + str(proj_id)+" and date_s<='" + each_result['date'] +"'"
            cur.execute(sql_get_act_each_total)
            results = cur.fetchall()       
            close_pgconn(cur,conn)        

            result_str = result_str+'{"date":"' + each_result['date'] +'",'+'"dayNumber":"' + str(each_result['number']) + '","totalNumber":"' + str(results[0][0]) +'"},'

    result_str = result_str[0:int(len(result_str))-1]    
    result_str = '{"tuple":[' + result_str +']}'        
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
        #print each_result['title']
        ###each_result['number'] = str(item[2])
        #result_str_each = each_result['title'] + "," + each_result['number']
        ###result_item.append(each_result)
        ###result_str = result_str+'{"title":"' + each_result['title'] +'",'+'"number":"' + each_result['number'] + '","id":"'+str(item[1])+'"},'
    #print result_item
    #return HttpResponse("<p>"+str(result_item)+"</p>")

    ###result_str = result_str[0:int(len(result_str))-1]    
    result_str = join_user 
    result_str = '{"tuple":"' + result_str +'"}'
    ###result_str = join_user 
    print result_str
    #result_str = result_str.replace("\","")
    #print result_str
    #json_total = {}
    #json_total['tuple'] = result_item

    #return json_total
    return result_str