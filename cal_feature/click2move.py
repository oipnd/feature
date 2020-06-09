import numpy as np
import os
def click2tomove(txtpath):
    f = open(txtpath)
    allines = f.readlines()
    arr =[]
    Time_keyup_mousemove = []
    Time_mousemove_keydown =[]
    Time_mousemove_mousedown =[]
    for j in range(len(allines)):
        if allines[j].split(' ')[0] == 'login':
            arr.append(allines[j])
    # print(arr)
    for i in range(2,len(arr) - 1):
        line1 = arr[i].split(' ')
        line2 = arr[i+1].split(' ')
        if (line2[1] == 'mousemove' and line1[1] == 'keyup') or (line2[1] == 'mousemove' and line1[1] == 'keyUp'):
            time = int(int(line2[4][:-1]) - int(line1[3][:-1]))
            Time_keyup_mousemove.extend([time])
        if (line2[1] == 'keydown' and line1[1] == 'mouseup') or (line2[1] == 'keyDown' and line1[1] == 'mouseup') or (line2[1] == 'keydown' and line1[1] == 'mousemove'):
            time1 = int(int(line2[3][:-1]) - int(line1[4][:-1]))
            Time_mousemove_keydown.extend([time1])
        if (line2[1] == 'mousedown' and line1[1] == 'mousemove') or (line2[1] == 'mouseDown' and line1[1] == 'mousemove'):
            time2 = int(int(line2[4][:-1]) - int(line1[4][:-1]))
            Time_mousemove_mousedown.extend([time2])
    f.close()
    return Time_keyup_mousemove,Time_mousemove_keydown,Time_mousemove_mousedown
def Statistic_para(list):
    st_mean = np.mean(list)
    st_std = np.std(list)
    st_var = np.var(list)
    # st_max = np.max(list)
    # st_min = np.min(list)
    # st_range =st_max -st_min
    coef_of_vari = st_std / st_mean
    final_fea = [st_mean,st_std,st_var,coef_of_vari]
    return final_fea

if __name__ == '__main__':
    path = "D:\data\pc"
    users=os.listdir(path)
    feature  =[]
    for user in users:
        timepath= path+user+os.sep
        timelist=os.listdir(timepath)
        for time in timelist:
            txtpath=timepath+time+os.sep
            txtlist=os.listdir(txtpath)
            for txt in txtlist:
                finallist=txtpath+txt
                time,time2,time1 = click2tomove(finallist)
                fea_fusion =Statistic_para(time) + Statistic_para(time2)
                feature.append(fea_fusion)
    final = np.array(feature)
    print(final[66])
    print(len(final[2]))
    print(type(final))
    print(len(final))











