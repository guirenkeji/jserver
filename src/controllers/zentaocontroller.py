# -*- coding: utf-8 -*-
# from flask import Flask,request,url_for,jsonify
from flask import Module,render_template,jsonify, redirect, request, session, g
from src.agentconfig import *
import httplib
import json
import urllib2 
import urllib
import logging
import cookielib
import requests

logging.basicConfig(level = logging.DEBUG)

zentao = Module(__name__)
@zentao.route('/agent/zentao')
def hello_zentao():
    return 'Hello zentao!'        
def login():                                                                      
    email = "fulisheng"                                         
    pwd = "1234567890"                                            
    data={"account":email,"password":pwd} 
    post_data=urllib.urlencode(data) 
    cj=cookielib.CookieJar()                 
    opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))                
    headers ={"User-agent":"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1"} 
    website = "http://zt.jm.com/zentao/user-login.json" 
    website1 = "http://zt.jm.com/zentao/project-story-8.json"                                        
    req=urllib2.Request(website,post_data,headers) 
    req1=urllib2.Request(website1,post_data,headers)                              
    content=opener.open(req)                                                    
    print content.read()
@zentao.route('/agent/1.0/zentao',methods=['POST'])        
def getZentaoInfo():
    s = requests.Session()
    bugkey_id = request.json['bugkey_id']
    account = request.json['account']
    password = request.json['password']
    url1 = zentao_url+'/user-login.json' #登陆地址
    url2 = zentao_url+'/bug-view-%s.json' %(bugkey_id) #需要登陆才能访问的页面地址
    data={"account":account,"password":password}
    headers = { "Accept":"text/html,application/xhtml+xml,application/xml;",
                "Accept-Encoding":"gzip",
                "Accept-Language":"zh-CN,zh;q=0.8",
                "Referer":"http://www.example.com/",
                "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
                }
    logging.info(s)
    res1 = s.post(url1,data=data)
    logging.info(s)
    res2 = s.post(url2)
    contentData = json.loads(res2.text)
    zentao_status =contentData['status']
    if zentao_status == 'success':
        
        contentData1 = contentData['data']
        logging.info(contentData1)
        #禅道问题解析data
        zentao_data = json.loads(contentData1)
        #需求标题
#         title = zentao_data['story']['title'] 
        #bug标题
        bug_title = zentao_data['bug']['title']
        logging.info(bug_title)
        logging.info(res1.content)
        logging.info(res2.text)
    else:
         logging.info('连接禅道接口  error ')
    data = {"status":"success","bug_title":bug_title}

    return jsonify(data)
#     content1 = json.dumps(res2.text, encoding="utf-8")
#     print res2.content#获得二进制响应内容
#     print res2.raw#获得原始响应内容,需要stream=True
#     print res2.raw.read(50)
#     print type(res2.text)#返回解码成unicode的内容
#     print res2.history#追踪重定向
#     print res2.cookies
#     print res2.cookies['example_cookie_name']
#     print res2.headers
#     print res2.headers['Content-Type']
#     print res2.headers.get('content-type')
#     print res2.json#讲返回内容编码为json
#     print res2.encoding#返回内容编码
#     print res2.status_code#返回http状态码
#     print res2.raise_for_status()#返回错误状态码


if __name__ == '__main__':
#     login()
#     httpdownloadpost()
    getZentaoInfo()