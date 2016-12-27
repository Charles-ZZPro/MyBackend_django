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

def get_user_info(request):
    cb_mine = request.GET.get('_cb_mine')
    result_item = cb_mine+"("+models.get_user_info()+")"
    #result_item = models.get_active_totalnums()
    #print result_item
    #print HttpResponse(json.dumps(result_item), content_type="application/json") 
    return HttpResponse(result_item, content_type="text/plain")      