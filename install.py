# -*- coding: UTF-8 -*- 
# import sys
# from testTeam.models import database,UserProfile,UserStatus
# from datetime import datetime
# if '-dropcreate' in sys.argv:
#     database.drop_database()
#     print(u'删除数据库完成')
# 
# database.create_database()
# print(u'创建数据库完成')
# 
# 
# session = database.get_session()
# 
# admin = UserProfile()
# admin.Email = 'admin@admin.com'
# admin.Nick = u'admin'
# admin.Password = 'admin'
# admin.Status = UserStatus.Enabled
# admin.IsAdmin = True
# admin.RegDate = datetime.now()
# session.add(admin)
# session.commit()
# session.close()
# print(u'PowerTeam安装完成')
