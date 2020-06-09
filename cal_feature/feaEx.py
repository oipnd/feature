# -*- coding: utf-8 -*-
"""
Created on Sun Dec 04 09:35:55 2016
# 键盘特征融合提取
@author: tql
"""

from math import ceil
import numpy as np

def featureEx(keyHoldTime):

   
#    for item in keyHoldTime:
    ht_Array=np.array(keyHoldTime)
    ht_Arraysort=sorted(ht_Array)

    ht_Array = np.abs(ht_Array)
    ht_mean=np.mean(ht_Array)
    ht_std=np.std(ht_Array)
    ht_var = np.var(ht_Array)
    ht_max=np.max(ht_Array)
    ht_min=np.min(ht_Array) 
    ht_range=ht_max-ht_min
    coef_of_vari = ht_std / ht_mean

    
    n=len(ht_Arraysort)
    if n%2!=0:
        ht_med=ht_Arraysort[int((n-1)/2)]
    else: ht_med=(ht_Arraysort[int(n/2)]+ht_Arraysort[int(n/2-1)])/2

    featureFinal=[ht_mean,ht_std,ht_var,ht_med,coef_of_vari,ht_max,ht_min,ht_range]

    return featureFinal
# keyHoldTime为字典
def specialitems(keyHoldTime,keyvalue):
    keyCode=keyHoldTime.keys()
    for item in keyCode:  
        
        if item==keyvalue:
            ht_Array=np.array(keyHoldTime[item])
            ave=np.mean(ht_Array)
            num=len(ht_Array)
     
            return ave,num   
        else: return 0,0
        
def specialfeaEx(keyHoldTime,keyDown_Up):
    count=0
    tol=0
    keycode=keyDown_Up.keys()
    for item in keycode:
        for i in range(len(keyDown_Up[item])):
            tol+=1
            if keyDown_Up[item][i]<0:
                count+=1
    minsradio=float(count)/tol

    
    shift,shiftnum=specialitems(keyHoldTime,'10')
    tab,tabnum=specialitems(keyHoldTime,'9')
    back,backnum=specialitems(keyHoldTime,'8')


    total=0
    key=keyHoldTime.keys()
    for i in key:
        total+=len(keyHoldTime[i])  
    specialradio=float(shiftnum+tabnum+backnum)/total
    specialfea=[minsradio]

    return specialfea
