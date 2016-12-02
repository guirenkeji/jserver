from src.controllers.common.svn.remote import RemoteClient
import logging
# from flask import Module,render_template,jsonify, redirect, request, session, g
# svn_repo_info = Module(__name__)
# 
# @svn_repo_info.route('/svn')
# def hello_svn_repo_info():
#     return 'Hello svn_repo_info!'
# @svn_repo_info.route('/1.0/svn',methods=['POST'])
def getSvnInfo():
    r = RemoteClient('http://192.168.23.133:8081/svn/test/branches',username='fls',password='123456')
    repos_info1 =  r.list()
    
    for i in repos_info1:
      print i
    repos_info =  r.info('jumore-wk37.w1c1')
    logging.info(repos_info)
    logs =  r.log_default(rel_filepath="jumore-wk37.w1c1")
    for y in logs:
       print y
    
    
#     return (repos_info,logs)


#     r.checkout('/tmp/working')
if __name__ == '__main__':
   getSvnInfo()