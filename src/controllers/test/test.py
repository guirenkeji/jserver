# from src.agentconfig import *
# agent_ip_list = AGENT_IP
# for i in agent_ip_list :
#     print i
# import datetime
# 
# d1 = datetime.datetime.strptime('2012-03-02 17:41:20', '%Y-%m-%d %H:%M:%S')
# 
# d2 = datetime.datetime.strptime('2012-03-02 17:41:20', '%Y-%m-%d %H:%M:%S')
# 
# if d1>d2:
#     print d1
# else:
#     print 'xiao:',d2    
#  
import operator 
l = [{'date': '2010-04-03 14:25:37','people': 1047, 'hits': 4522},  
         {'date': '2010-04-03 14:25:35', 'people': 617, 'hits': 2582},  
         {'date': '2012-04-03 15:25:35', 'people': 736, 'hits': 3277}] 
l1 = sorted( l, key = operator.itemgetter('date'),reverse =True )
print l1
