# -*- coding: UTF-8 -*-
from flask import Module,render_template,jsonify, redirect, request, session, g
from src.agentconfig import *
import os
import logging
import json
import httplib
import re
import operator
logging.basicConfig(level=logging.DEBUG)
nexusServer = Module(__name__)
@nexusServer.route('/nexus')
def hello_svn_repo_info():
    print dir(request)
    return 'Hello nexusServer_info!'
@nexusServer.route('/nexus/1.0/meta',methods=['POST'])
def getNexusMetadata (par=None):
#     version = request.josn['version']
#     username = request.json['username']
#     password = request.json['password']
#     nexus_repos_url = request.json['nexus_repos_url']
    layer1 = 'com_acme2'
    layer2 = 'disconf-tool'
    nexus_metadata = os.popen('curl -v \
                        -u admin:admin123 \
                        http://192.168.23.133:9002/nexus/service/local/repositories/pro/content/%s/%s/ --connect-timeout 10 ' %(layer1,layer2)).readlines() 
    metadata_list = nexusMetaAnalysis(nexus_metadata,layer2)
    logging.info(metadata_list)
    return jsonify({'status':'ok','data':metadata_list})  
@nexusServer.route('/nexus/1.0/package/delete',methods=['POST'])
def deleteFile():
    package_id = request.josn['package_id']
    
    delete_file = os.popen('curl -X  DELETE \
                            -u %s:%s \
                             %s/content/repositories/pro/com_acme_widgets/ ' )
    logging.info(delete_file)
    return delete_file

#===============================================================================
# 解析xml表达式匹配。后续repos可能有多层。目前定义3层，layer1为项目，layer2为模块，layer3为版本及文件
#===============================================================================
def nexusMetaAnalysis (nexus_metadata,layer2):
    file_info_list = []
    c1 = []
    metadata_tuple = xmlAnalysis(nexus_metadata)
    for i in metadata_tuple:
        if 'false' in i:
#===============================================================================
# i[1]layer3文件版本,c2文件列表
#===============================================================================
            c2 = nexusFileSide (i[0],i[1])
            c1.append({'layer3_resourceURI':i[0],'layer3_text':i[1],'layer3_file':c2})
#===============================================================================
# 包按上传时间排序            
#===============================================================================
            file_info_list.append(c2)
            file_info_list = sorted( file_info_list, key = operator.itemgetter('file_updatetime'),reverse =True )
#===============================================================================
# c3获取当前最新包            
#===============================================================================
    file_name = file_info_list[0]['file_name']
    file_updatetime = file_info_list[0]['file_updatetime']
    file_url = file_info_list[0]['file_url']
    c3 = {'file_name':file_name,'file_updatetime':file_updatetime,'file_url':file_url}
#===============================================================================
# 添加最新包到返回值       
#===============================================================================
    c1.append({'file_last_modified':c3})        
    return c1
def nexusFileSide (file_url,version):
    file_info = {}
    nexus_file_metadata = os.popen('curl -v \
                        -u admin:admin123 \
                        %s --connect-timeout 10 ' %(file_url)).readlines() 
    metadata_tuple = xmlAnalysis(nexus_file_metadata)
    for i in  metadata_tuple:
        if i[1].split('.')[-1] in ['zip','jar','war','exe','gz','rar','tar']:
#===============================================================================
# 定为nexus时间格式。0 UTC    
#===============================================================================
            file_info = {'file_url':i[0],'file_name':i[1],'file_updatetime':i[3].split('.0 UTC')[0],'file_size':float(i[4])/(1024*1024)}
    return file_info
def xmlAnalysis(nexus_metadata):
    metadata_list = []
    for i in nexus_metadata:
        metadata_list.append(i.strip('\n').strip())
    metadata_str = ''.join(metadata_list)
#===============================================================================
# 表达式匹配    
#===============================================================================
    metadata_tuple= re.compile(r"(?<=<resourceURI>)(.*?)(?=</resourceURI>).+?(?<=<text>)(.*?)(?=</text>).+?(?<=<leaf>)(.*?)(?=</leaf>).+?(?<=<lastModified>)(.*?)(?=</lastModified>).+?(?<=<sizeOnDisk>)(.*?)(?=</sizeOnDisk>)") 
    metadata_tuple = metadata_tuple.findall(metadata_str)
    return  metadata_tuple        
if __name__ ==  '__main__':
    print 'nexus'


    
    
    
      