# -*- coding: UTF-8 -*-
from flask import Module,render_template,jsonify, redirect, request, session, g
from src.agentconfig import *
import os
import logging
import json
import httplib
logging.basicConfig(level=logging.DEBUG)
nexusServer = Module(__name__)
@nexusServer.route('/nexus')
def hello_svn_repo_info():
    print dir(request)
    return 'Hello nexusServer_info!'
@nexusServer.route('/nexus/1.0/meta',methods=['POST'])
def getMetadata ():
#     version = request.josn['version']
#     username = request.json['username']
#     password = request.json['password']
#     nexus_repos_url = request.json['nexus_repos_url']
    nexus_metadata = os.popen('curl -v \
                        -u admin:admin123 \
                        http://192.168.23.133:9002/nexus/service/local/repositories/pro/content/com_acme_widgets/ --connect-timeout 10 ').readlines()
    for i in nexus_metadata:
        print i.strip('\n')                    
    
    logging.info(nexus_metadata)
    return 'nexus_metadata'     
def delete_file():
    delete_file = os.popen('curl -X  DELETE \
                            -u %s:%s \
                             %s/content/repositories/pro/com_acme_widgets/ ' )
    logging.info(delete_file)
    return (delete_file)

 
                
if __name__ ==  '__main__':
    print '5555555'


    
    
    
      