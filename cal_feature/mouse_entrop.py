import os
import numpy
path = r'C:\Users\niuniu\Desktop\3'
file_list = os.listdir(path)
for file in file_list:
    file_path = path + os.sep +file
    txt_list= os.listdir(file_list)
    for txt in txt_list:
        txt_path = file_path + os.sep + txt
        f = open(txt_path).readlines()
        login_collect = []
        for line in f:
            line = line.strip().split()
            if not line:
                continue
            else:
                if line[0] == 'login':
                    login_collect.append(line)
        mark = 1
        dic = {}
        for i in range(len(login_collect)):
            segment_move = []
            if login_collect[i][1] == 'mousemove'and login_collect[i+1][1] != 'mousemove':
                segment_move.append(login_collect[i])
            dic[mark] = segment_move
            mark +=1
            continue

print(dic)

