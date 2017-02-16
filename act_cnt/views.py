# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
import psycopg2
import json
from act_cnt import models
# Create your views here.

def first_page(request):
    return HttpResponse("<p>Gotcha!!!!</p>")

def get_active_totalnums(request):
    cb_mine = request.GET.get('_cb_mine')
    result_item = cb_mine+"("+models.get_active_totalnums()+")"
    #result_item = models.get_active_totalnums()
    #print result_item
    #print HttpResponse(json.dumps(result_item), content_type="application/json") 
    return HttpResponse(result_item, content_type="text/plain")  
    #return result_item

def get_active_dailynums(request):
    proj_id = request.GET.get('proj_id')
    cb_mine = request.GET.get('_cb_mine')
    result_item = cb_mine+"("+models.get_active_dailynums(proj_id)+")"
    #print result_item
    #return HttpResponse(json.dumps(result_item,ensure_ascii=False), content_type="application/json") 
    return HttpResponse(result_item, content_type="text/plain")  
    #return result_item	

def get_active_dailynums_filter(request):
    proj_id = request.GET.get('proj_id')
    cb_mine = request.GET.get('_cb_mine')
    date_range = request.GET.get('value')
    result_item = cb_mine+"("+models.get_active_dailynums_filter(proj_id,date_range)+")"
    #print result_item
    #return HttpResponse(json.dumps(result_item,ensure_ascii=False), content_type="application/json") 
    return HttpResponse(result_item, content_type="text/plain")  
    #return result_item 

def insert_daily_fake_data(request):
    print "fffffffff"
    return HttpResponse(models.insert_daily_fake_data())

def insert_daily_fake_data_fortesting_rate(request):
    print "fffffffff"
    return HttpResponse(models.insert_daily_fake_data_fortesting_rate())    
    

def insert_daily_fake_data_fortesting(request):
    print "fffffffff"
    return HttpResponse(models.insert_daily_fake_data_fortesting())

def get_list_by_date(request):
    proj_id = request.GET.get('proj_id')
    cb_mine = request.GET.get('_cb_mine')
    result_item = models.get_list_by_date()
    #result_item = cb_mine+"("+models.get_list_by_date()+")"
    #print result_item
    #return HttpResponse(json.dumps(result_item,ensure_ascii=False), content_type="application/json") 
    return HttpResponse(result_item, content_type="text/plain")  
    #return result_item 

def get_list_by_country(request):
    proj_id = request.GET.get('proj_id')
    cb_mine = request.GET.get('_cb_mine')
    result_item = models.get_list_by_country()
    #result_item = cb_mine+"("+models.get_list_by_date()+")"
    #print result_item
    #return HttpResponse(json.dumps(result_item,ensure_ascii=False), content_type="application/json") 
    return HttpResponse(result_item, content_type="text/plain")  
    #return result_item     

def get_user_info(request):
    cb_mine = request.GET.get('_cb_mine')
    result_item = cb_mine+"("+models.get_user_info()+")"
    #result_item = models.get_active_totalnums()
    #print result_item
    #print HttpResponse(json.dumps(result_item), content_type="application/json") 
    return HttpResponse(result_item, content_type="text/plain")      


def get_top5_lively_country(request):
    proj_id = request.GET.get('proj_id')
    cb_mine = request.GET.get('_cb_mine')
    result_item = cb_mine+"("+models.get_top5_lively_country(proj_id)+")"
    #print result_item
    #return HttpResponse(json.dumps(result_item,ensure_ascii=False), content_type="application/json") 
    return HttpResponse(result_item, content_type="text/plain")  

def get_map_data(request):
    proj_id = request.GET.get('proj_id')
    cb_mine = request.GET.get('_cb_mine')
    result_item = cb_mine+"("+models.get_map_data(proj_id)+")"
    #print result_item
    #return HttpResponse(json.dumps(result_item,ensure_ascii=False), content_type="application/json") 
    return HttpResponse(result_item, content_type="text/plain")  

####################
def get_tongji_to_frontpage(request):
    user_name = request.GET.get('user_name')
    cb_mine = request.GET.get('_cb_mine')
    date_1 = request.GET.get('value1')
    date_2 = request.GET.get('value2')
    result_item = cb_mine+"("+models.get_tongji_to_frontpage(user_name,date_1,date_2)+")"
    #print result_item
    #return HttpResponse(json.dumps(result_item,ensure_ascii=False), content_type="application/json") 
    return HttpResponse(result_item, content_type="text/plain") 

def get_user_info_list(request):
    user_name = request.GET.get('user_name')
    cb_mine = request.GET.get('_cb_mine')
    name_filter = request.GET.get('value')
    result_item = cb_mine+"("+models.get_user_info_list(user_name,name_filter)+")"
    #print result_item
    #return HttpResponse(json.dumps(result_item,ensure_ascii=False), content_type="application/json") 
    return HttpResponse(result_item, content_type="text/plain")     

def put_logintime(request):
    print "fffffffff"
    user_name = request.GET.get('user_name')    
    cb_mine = request.GET.get('_cb_mine')
    # name_filter = request.GET.get('value')
    result_item = cb_mine+"("+models.put_logintime(user_name)+")"
    #print result_item
    #return HttpResponse(json.dumps(result_item,ensure_ascii=False), content_type="application/json") 
    return HttpResponse(result_item, content_type="text/plain")  

def get_user_logintime_list(request):
    print "fffffffff"
    user_name = request.GET.get('user_name')    
    cb_mine = request.GET.get('_cb_mine')
    # name_filter = request.GET.get('value')
    result_item = cb_mine+"("+models.get_user_logintime_list(user_name)+")"
    #print result_item
    #return HttpResponse(json.dumps(result_item,ensure_ascii=False), content_type="application/json") 
    return HttpResponse(result_item, content_type="text/plain") 

def change_passwd(request):
    print "fffffffff"
    user_name = request.GET.get('user_name')    
    passwd = request.GET.get('passwd')      
    cb_mine = request.GET.get('_cb_mine')
    # name_filter = request.GET.get('value')
    result_item = cb_mine+"("+models.change_passwd(user_name, passwd)+")"
    #print result_item
    #return HttpResponse(json.dumps(result_item,ensure_ascii=False), content_type="application/json") 
    return HttpResponse(result_item, content_type="text/plain")

def froze_accout(request):
    print "fffffffff"
    user_name = request.GET.get('user_name')    
    passwd = request.GET.get('passwd')      
    cb_mine = request.GET.get('_cb_mine')
    # name_filter = request.GET.get('value')
    result_item = cb_mine+"("+models.froze_accout(user_name)+")"
    #print result_item
    #return HttpResponse(json.dumps(result_item,ensure_ascii=False), content_type="application/json") 
    return HttpResponse(result_item, content_type="text/plain")

def change_role(request):
    print "fffffffff"
    user_name = request.GET.get('user_name')    
    role = request.GET.get('role')      
    cb_mine = request.GET.get('_cb_mine')
    # name_filter = request.GET.get('value')
    result_item = cb_mine+"("+models.change_role(user_name, role)+")"
    #print result_item
    #return HttpResponse(json.dumps(result_item,ensure_ascii=False), content_type="application/json") 
    return HttpResponse(result_item, content_type="text/plain")

def get_rolemenues_info(request):
    print "fffffffff"
    # user_name = request.GET.get('user_name')    
    cb_mine = request.GET.get('_cb_mine')
    # name_filter = request.GET.get('value')
    result_item = cb_mine+"("+models.get_rolemenues_info()+")"
    #print result_item
    #return HttpResponse(json.dumps(result_item,ensure_ascii=False), content_type="application/json") 
    return HttpResponse(result_item, content_type="text/plain")     

def get_projs(request):
    print "fffffffff"
    # user_name = request.GET.get('user_name')    
    cb_mine = request.GET.get('_cb_mine')
    # name_filter = request.GET.get('value')
    result_item = cb_mine+"("+models.get_projs()+")"
    #print result_item
    #return HttpResponse(json.dumps(result_item,ensure_ascii=False), content_type="application/json") 
    return HttpResponse(result_item, content_type="text/plain") 

def change_related_project(request):
    print "fffffffff"
    user_name = request.GET.get('user_name')    
    cb_mine = request.GET.get('_cb_mine')
    arr_projs = request.GET.get('arr_projs')
    result_item = cb_mine+"("+models.change_related_project(user_name,arr_projs)+")"
    #print result_item
    #return HttpResponse(json.dumps(result_item,ensure_ascii=False), content_type="application/json") 
    return HttpResponse(result_item, content_type="text/plain") 

def change_comment(request):
    print "fffffffff"
    user_name = request.GET.get('user_name')    
    cb_mine = request.GET.get('_cb_mine')
    comment = request.GET.get('comment')
    result_item = cb_mine+"("+models.change_comment(user_name,comment)+")"
    #print result_item
    #return HttpResponse(json.dumps(result_item,ensure_ascii=False), content_type="application/json") 
    return HttpResponse(result_item, content_type="text/plain") 
    
def insert_formatted_data_to_db_pass(request):
    print "fffffffff"
    file_name = request.GET.get('file_name')
    time = request.GET.get('time')    
    proj_name = request.GET.get('proj_name')      
    return HttpResponse(models.insert_formatted_data_to_db_pass(file_name,time,proj_name)) 

def put_active_datelist_into_db(request):
    print "fffffffff"
    # arr = request.GET.get('arr')
    # time = request.GET.get('time')    
    # proj_name = request.GET.get('proj_name')      
    return HttpResponse(models.put_active_datelist_into_db()) 

def put_daily_active_total_2016(request):
    print "fffffffff"
    # file_name = request.GET.get('file_name')
    # time = request.GET.get('time')    
    # proj_name = request.GET.get('proj_name')      
    return HttpResponse(models.put_daily_active_total_2016())  

def insert_formatted_data_to_db_pass_new_2017(request):
    print "fffffffff"
    # file_name = request.GET.get('file_name')
    # time = request.GET.get('time')    
    # proj_name = request.GET.get('proj_name') 
    return HttpResponse(models.insert_formatted_data_to_db_pass_new_2017())      
  
def get_all_table_name(request):
    print "fffffffff"
    # file_name = request.GET.get('file_name')
    # time = request.GET.get('time')    
    # proj_name = request.GET.get('proj_name')      
    return HttpResponse(models.get_all_table_name()) 
    
           
####################
def putting_data(request):
    print "fffffffff"
    return HttpResponse(models.putting_data())   
    
def insert_formatted_data_to_db(request):
    print "fffffffff"
    file_name = request.GET.get('file_name')
    time = request.GET.get('time')    
    proj_name = request.GET.get('proj_name')      
    return HttpResponse(models.insert_formatted_data_to_db(file_name,time,proj_name))   

def create_new_table_for_daily_active(request):
    print "fffffffff"    
    return HttpResponse(models.create_new_table_for_daily_active()) 

def insert_all_daily_data(request):
    print "fffffffff"    
    return HttpResponse(models.insert_all_daily_data())                 

def insert_formatted_data_to_db_imsi(request):
    print "fffffffff"
    return HttpResponse(models.insert_formatted_data_to_db_imsi())   
     
    