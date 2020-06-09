# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 20:45:30 2019

@author: niuniu
"""

#import os
#
#path0 = r'C:\Users\niuniu\Desktop\nae'
#file_list = os.listdir(path0)
#for file in file_list:
#    path = path0 +os.sep + file
#    txt_list = os.listdir(path)
#    for txt in txt_list:
##        print(txt)
#        new_name = 'n_'+ txt
#        print(new_name)
#        each_path = path +os.sep+ txt
##        print(each_path,path+os.sep+new_name)
#        print(each_path)
#        os.rename(each_path,path+os.sep+new_name)
#    os.rename(each_path,"C:\Users\niuniu\Desktop\dd\robot9_1_.txt")
import os 
#print(os.getcwd())
path = r'C:\Users\niuniu\Desktop\name'
txt_list = os.listdir(path)
print(txt_list)
for txt in txt_list:
	new_name = 'm_'+ txt
# 为新命名的文件添加路径
	oldname_path = path + os.sep +txt
	newname_newpath = path + os.sep +new_name
	os.rename(oldname_path,newname_newpath)
txt_list = os.listdir(path)
print(txt_list)