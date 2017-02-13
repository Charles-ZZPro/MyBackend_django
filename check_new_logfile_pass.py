#-*-coding:utf-8-*-
from __future__ import unicode_literals
import gzip 
import tarfile
import os,os.path,datetime
from django.db import models
import psycopg2
import sys
import datetime
import random
import shutil
import urllib2

#from pyinotify import WatchManager, Notifier, ProcessEvent, IN_DELETE, IN_CREATE, IN_MODIFY

reload(sys)
sys.setdefaultencoding('utf-8')

##### Script of Checking
###check new logfile. If new logfile is released, call the insert-to-db interface
#####

base_dir="/home/charles/log/"
l=os.listdir(base_dir)
l.sort(key=lambda fn: os.path.getmtime(base_dir+fn) if not os.path.isdir(base_dir+fn) else 0)
d=datetime.datetime.fromtimestamp(os.path.getmtime(base_dir+l[-1]))
print('Newest file is : '+l[-1]+"，Time : "+d.strftime("%Y-%m-%d %H:%M:%S"))
time = d.strftime("%Y-%m-%d-%H:%M:%S")

targetLine = "";  
file=open("logFileList.txt","r")
mLines = file.readlines();
targetLine = mLines[-1];
file.close()
#print mLines

print('Last file recorded is : '+targetLine)

###### get project name
proj_name = "Sherlock"
######

if targetLine!=l[-1]:
    f=open("logFileList.txt","a")
    f.write("\n")
    f.write(l[-1])
    f.close()
    url_path = "http://localhost:8099/act_cnt/insert_formatted_data_to_db_pass/?file_name="+l[-1]+"&time="+time+"&proj_name="+proj_name
    s = urllib2.urlopen(url_path).read()