# -*- coding: UTF-8 -*-
from flask import Module,render_template,jsonify, redirect, request, session, g
from src.agentconfig import *
import os
import logging
import json
import httplib
logging.basicConfig(level=logging.DEBUG)
nexus = Module(__name__)
@nexus.route('/agentAPI/nexus')
def hello_svn_repo_info():
    print dir(request)
    return 'Hello nexus_info!'
@nexus.route('/agentAPI/nexus/1.0/push',methods=['POST'])
def pushToNexus ():
#===============================================================================
# 单个文件curl上传
#===============================================================================
    data = request.get_json()
    for i in AGENT_IP:
        ip = i.split('-')[0]
        label = i.split('-')[1]
        httpPushPost (ip,data)
@nexus.route('/agentAPI/nexus/1.0/pull',methods=['POST'])
def downloadFromNexus ():
    data = request.get_json()
    for i in AGENT_IP:
        httpPushPost (i,data)
    httpDownloadPost(data)
  
def httpPushPost (agent_ip,agent_port,data):
    try:
        data = json.dumps(data)
        httpClient = httplib.HTTPConnection(agent_ip,agent_port, timeout=30) 
        logging.info(data)
        httpClient.request("POST",'/agent/nexus/1.0/push',data,{'Content-Type': 'application/json'})
        response = httpClient.getresponse()
        print response
    
    except Exception, e:
        print e  
def httpDownloadPost (agent_ip,agent_port,data):
    try:
        data = json.dumps(data)
        httpClient = httplib.HTTPConnection(agent_ip,agent_port, timeout=30) 
        logging.info(data)
        httpClient.request("POST",'/agent/nexus/1.0/pull',data,{'Content-Type': 'application/json'})
        response = httpClient.getresponse()
        print response
    
    except Exception, e:
        print e   
# def delete_file():
#     delete_file = os.popen('curl -X  DELETE \
#                             -u %s:%s \
#                              %s/content/repositories/pro/com_acme_widgets/ ' %(username,password,nexus_repos_url))
#     logging.info(delete_file)
#     return (delete_file)
#===============================================================================
# http://192.168.23.133:9002/nexus/content/repositories/pro/com_acme_widgets/disconf-tool/2.6.28/disconf-tool-2.6.28.zip
#===============================================================================

# def get_nexus_info():
#     file_list = os.popen('curl -X  DELETE \
#                             -u admin:admin123 \
#                             http://192.168.23.133:9002/nexus/content/repositories/pro/com_acme_widgets/ --connect-timeout 10 ').readlines()
#                             
#     logging.info(file_list)
#     print dir(file_list)                 
if __name__ ==  '__main__':
    print '5555555'
#     pushToNexus()
#     getNexus()
#     delete_file()
#     get_nexus_info()
    
    
    
    
      