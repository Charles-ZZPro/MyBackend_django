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
    url(r'^putting_data/$', views.putting_data), 
    url(r'^insert_formatted_data_to_db/$', views.insert_formatted_data_to_db),  
    url(r'^create_new_table_for_daily_active/$', views.create_new_table_for_daily_active), 
    url(r'^insert_all_daily_data/$', views.insert_all_daily_data),          
    url(r'^insert_formatted_data_to_db_imsi/$', views.insert_formatted_data_to_db_imsi), 
    url(r'^change_related_project/$', views.change_related_project),    
              
#############
    url(r'^get_tongji_to_frontpage/$', views.get_tongji_to_frontpage),  
    url(r'^get_tongji_to_frontpage_proj/$', views.get_tongji_to_frontpage_proj),     
    url(r'^get_user_info_list/$', views.get_user_info_list),
    url(r'^put_logintime/$', views.put_logintime),  
    url(r'^get_user_logintime_list/$', views.get_user_logintime_list),
    url(r'^change_passwd/$', views.change_passwd),    
    url(r'^froze_accout/$', views.froze_accout),   
    url(r'^change_role/$', views.change_role), 
    url(r'^get_rolemenues_info/$', views.get_rolemenues_info),     
    url(r'^get_projs/$', views.get_projs),         
    url(r'^change_comment/$', views.change_comment),     
    url(r'^insert_formatted_data_to_db_pass/$', views.insert_formatted_data_to_db_pass), 
    url(r'^put_active_datelist_into_db/$', views.put_active_datelist_into_db), 
    url(r'^put_daily_active_total_2016/$', views.put_daily_active_total_2016),  
    url(r'^insert_formatted_data_to_db_pass_new_2017/$', views.insert_formatted_data_to_db_pass_new_2017),  
    url(r'^get_all_table_name/$', views.get_all_table_name),   
    url(r'^get_a/$', views.get_a),   
    url(r'^get_b/$', views.get_b),      
    url(r'^insert_subchannel_into_db/$', views.insert_subchannel_into_db),    
    url(r'^add_columns_to_dailyactive_tables/$', views.add_columns_to_dailyactive_tables),   
    url(r'^add_columns_to_duli_tables/$', views.add_columns_to_duli_tables),    
    url(r'^put_total_active_II/$', views.put_total_active_II),   
    url(r'^add_columns_to_total_tables/$', views.add_columns_to_total_tables),    
    url(r'^check_files_for_updated/$', views.check_files_for_updated),          
           
      
#############                
]
#http://120.77.179.136/