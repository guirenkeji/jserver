# -*- coding: UTF-8 -*-
import os
import subprocess
import logging
import time
import sys
logging.basicConfig(level=logging.DEBUG)
from_branch = os.environ['FROM_BRANCH']
to_branch = os.environ['TO_BRANCH']
svn_message = os.environ['MESSAGE']
# from_branch = "http://192.168.23.133:81/svn/test/trunk/jumore/"
# to_branch = "http://192.168.23.133:81/svn/test/branches/jumore-wk56/"
# svn_message = "#tag online 'jumore-test' Cpoy From@"
def branch():
    list = []
    try:
        
        branch_info_list = os.popen('svn info %s' %(from_branch)).readlines()
        to_branch_info = os.popen('svn info %s' %(to_branch)).readlines()#判断分支文件是否存在
        if to_branch_info==[]:
            logging.info(branch_info_list)
            for i in branch_info_list :
                if i !='\n':
                    i = i.strip('\n')
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
            messages = svn_message.split('@')
#===============================================================================
# windows @后面中文GBK字符转换        
#===============================================================================
            utf8Data = messages[1]
            unicodeData = utf8Data.decode("UTF-8")
            gbkData = unicodeData.encode("GBK")
            branch_tag = os.popen('svn copy %s %s -m "%s %s@%s %s%s"' 
                                   %(from_branch,to_branch,messages[0],from_branch,last_commit,last_date,gbkData)).readlines()
            logging.info(to_branch)
            logging.info(branch_tag)
        else:
            print  "已经存在分支文件"  
            sys.exit(1)
            
    except ValueError as e:
            print e
            sys.exit(1)
                       
if __name__ ==  '__main__':
    branch()
 