# -*- coding: UTF-8 -*-
import os
import subprocess
import logging
import time
logging.basicConfig(level=logging.DEBUG)
# from_merge_branch = os.environ['BRANCH']
from_merge_branch = 'http://192.168.23.133:8081/svn/test/branches/jumore-wk37.w1c1'
#===============================================================================
# 通过注释，判断是否合并到release发布分支 
#===============================================================================
provide_commit_message = '#mergeBranch#' #svn提供commit注释
def mergeDecide():
    try:
        merge_info = os.popen('svn log -l 1 %s' %(from_merge_branch)).readlines()
#===============================================================================
# commit注释提供#mergeBranch#字符串，才能执行合并
#===============================================================================
        data_list = []
        for i in merge_info:
            i = i.strip('\n')
            data_list.append(i) 
        data_list = data_list[3]
        print data_list
        if provide_commit_message in data_list:
            mergeBranch()
        logging.info(merge_info)     
    except Exception,e:
         print e  
def mergeBranch():
    print os.path.abspath(os.curdir)
    try:
        list = []
        merge_update_info = os.popen('svn update').readlines()
        logging.info(merge_update_info)
        merge_info_list = os.popen('svn info %s' %(from_merge_branch)).readlines()
        logging.info(merge_info_list)
        for i in merge_info_list :
            if i !='\n':
                i = i.strip('\n')
                print i
                p =i.split(':',1)
                list.append(p)
#============================================================================
# 当前版本信息
#============================================================================
        svn_info_data = dict(list)
        last_author = svn_info_data['Last Changed Author']
        last_commit = svn_info_data['Last Changed Rev']
        last_date = svn_info_data['Last Changed Date']
        last_date = last_date.split('+')[0]
        merge = os.popen('svn merge --accept p %s' %(from_merge_branch)).readlines()
        print merge
        if merge == []:
            raise ValueError,"merge_branch_error :"+ from_merge_branch
#               raise merge_branch_error
#===============================================================================
# 获取当前分支状态，判断是否能push操作
#===============================================================================
        branch_status = os.popen('svn status').readlines()
        for i in  branch_status:
            status_list = i.strip('\n')
            logging.info("svn branch status :"+status_list)
#             file = i.split('')
            if 'C' in status_list.split(" "):
                file = status_list.split(" ")[-1]
                svnConflict(file)
            if 'Summary of conflicts' in status_list:
                print "Summary of conflicts"
                break
#             return 'fail'
        else:
            push_origin = os.popen('svn commit -m "merge from %s@%s@%s@%s"' %(from_merge_branch,last_author,last_commit,last_date)).readlines()
            logging.info('push_origin ok')
#             return "ok"
    except ValueError as e:
#     except  merge_branch_error:
            print 'e'
def svnCommit(merge_from_url,):
    try:
        merge_info = os.popen('svn commit -m %s' %()).readlines()
        commit_message = ""
        logging.info(merge_info)
    except Exception,e:
         print e   
def svnContlictLog(log_list,file):
    try:
        data_list = []
        logging.info(log_list)
        for i in log_list:
            i = i.strip('\n')
            data_list.append(i) 
        print data_list      
        data_list = data_list[1]
        logging.info(data_list)
#===============================================================================
# 获取目录下文件最新版本号及提交人
#===============================================================================
        upnew_version = data_list.split('|')[0]
        upnew_author = data_list.split('|')[1]
        logging.info(upnew_version + upnew_author)
        return ({'contlict_file':file,'upnew_version':upnew_version,'upnew_author':upnew_author})
    except Exception,e:
         print e  
def svnConflict(win_file):
    try:
#===============================================================================
# windows路径格式，获取文件用户及版本
#===============================================================================
#         win_file = 'src\__init__.py'
        file = win_file.replace('\\',"/")
        branch_log_list = os.popen('svn log -l 1 %s/%s' %(from_merge_branch,file)).readlines()
        local_log_list = os.popen('svn log -l 1  %s' %(file)).readlines()
        branch_log_list = svnContlictLog(branch_log_list,file)
        local_log_list =  svnContlictLog(local_log_list,file)
        logging.info(branch_log_list)
        logging.info(local_log_list)
#===============================================================================
# 冲突文件处理        
#===============================================================================
#         logging.info(merge_info)
    except Exception,e:
         print e 
# def sys_command_outstatuserr():
#     timeout=5
#     cmd = 'svn log -l 1 -q http://192.168.23.133:8081/svn/test/branches/jumore-wk37.w1c1/src/svn/svn.test3/wk37w2c3.py' 
#     p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
#     t_beginning = time.time()
#     seconds_passed = 0
#     while True:
#         if p.poll() is not None:
#             res = p.communicate()
#             exitcode = p.poll() if p.poll() else 0
#             return res[0], exitcode, res[1]
#         seconds_passed = time.time() - t_beginning
#         if timeout and seconds_passed > timeout:
#             p.terminate()
#             out, exitcode, err = '', 128, '执行系统命令超时'
#             return out, exitcode, err
#         time.sleep(0.1)         
#     print "test"                               
if __name__ ==  '__main__':
#     mergeDecide()
    mergeBranch()
 