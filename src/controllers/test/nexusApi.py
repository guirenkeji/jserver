# -*- coding: UTF-8 -*-
import requests
import os
import logging
logging.basicConfig(level=logging.DEBUG)
nexus_repos_url = 'http://192.168.23.133:9002/nexus'
username = 'admin'
password = 'admin123'
file_name = 'war.zip'
r='pro'
g='com_acme_widgets'
a='disconf-tool'
v='2.6.30'
p='zip'
file_path = 'D:/tool'
# nexus = Module(__name__)
# @nexus.route('/nexus')
def hello_svn_repo_info():
    return 'Hello nexus_info!'
def pushToNexus ():
#===============================================================================
# 单个文件curl上传
#===============================================================================
    print os.path.abspath(os.curdir)
    try:
        file_push_repos = os.popen('curl -v \
                            -F "r=%s" \
                            -F "g=%s" \
                            -F "a=%s" \
                            -F "v=%s" \
                            -F "p=%s" \
                            -F "file=@%s/%s" \
                            -u %s:%s \
                            %s/service/local/artifact/maven/content'
#                                                             service/local/artifact/maven/content
                            %(r,g,a,v,p,file_path,file_name,username,password,nexus_repos_url)).readlines()
                 
        if file_push_repos==[] or 'error' in file_push_repos[0] :
            raise ValueError,"file push error :"+file_name                 

    except ValueError as e:
         print e
    
    logging.info(file_push_repos)
def getNexus ():
    
   
    push_repos = os.popen('curl -v \
                        -u admin:admin123 \
                        %s/service/local/attributes/pro/com_acme_widgets/content/').readlines()
    
    logging.info(push_repos)    
def delete_file():
    delete_file = os.popen('curl -X  DELETE \
                            -u %s:%s \
                             %s/content/repositories/pro/com_acme_widgets/ ' %(username,password,nexus_repos_url))
#===============================================================================
# http://192.168.23.133:9002/nexus/content/repositories/pro/com_acme_widgets/disconf-tool/2.6.28/disconf-tool-2.6.28.zip
#===============================================================================
    logging.info(delete_file)
    return (delete_file)
def get_nexus_info():
    file_list = os.popen('curl -X  DELETE \
                            -u admin:admin123 \
                            http://192.168.23.133:9002/nexus/content/repositories/pro/com_acme_widgets/ --connect-timeout 10 ').readlines()
                            
#     return (nexus_repos_info)
    logging.info(file_list)
    print dir(file_list)
if __name__ ==  '__main__':
    pushToNexus()
#     getNexus()
#     delete_file()
#     get_nexus_info()
    
    
    
    
      