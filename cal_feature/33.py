import array as arr
txt_path  = r'C:\Users\niuniu\Desktop\3\12\2150300072_1_1.txt'
f = open(txt_path).readlines()
login_collect = []
for line in f:
    line = line.strip().split()
    if not line:
        continue
    else:
        if line[0] == 'login':
            login_collect.append(line)
print(login_collect)
mark= 0
dic = {}
for i in range(len(login_collect)):
    segment_move = []
    while login_collect[i][1] == 'mousemove':
        segment_move.append(login_collect[i])
        i+= 1

    while login_collect[i][1] != 'mousemove':
              i +=1

print(segment )
# for i in dic.keys():
#     if dic[i].
# print(dic.keys())
