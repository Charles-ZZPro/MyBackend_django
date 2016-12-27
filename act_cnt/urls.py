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
    url(r'^get_user_info/$', views.get_user_info),      
]