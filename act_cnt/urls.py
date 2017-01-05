#-*-coding:utf-8-*-
from django.conf.urls import include, url
from act_cnt import views

urlpatterns = [
    url(r'^$', views.first_page),
    url(r'^get_active_totalnums/$', views.get_active_totalnums),
    #url(r'^get_active_dailynums/(.+)/$', views.get_active_dailynums),    
    url(r'^get_active_dailynums/$', views.get_active_dailynums),  
    url(r'^get_active_dailynums_filter/$', views.get_active_dailynums_filter),      
    url(r'^insert_daily_fake_data/$', views.insert_daily_fake_data),  
    url(r'^insert_daily_fake_data_fortesting/$', views.insert_daily_fake_data_fortesting),      
    url(r'^insert_daily_fake_data_fortesting_rate/$', views.insert_daily_fake_data_fortesting_rate),   
    url(r'^get_list_by_date/$', views.get_list_by_date),       
    url(r'^get_list_by_country/$', views.get_list_by_country),     
    url(r'^get_user_info/$', views.get_user_info),    
    url(r'^get_top5_lively_country/$', views.get_top5_lively_country),   
    url(r'^get_map_data/$', views.get_map_data),        
]