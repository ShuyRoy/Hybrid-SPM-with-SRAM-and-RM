"""
去掉重复的那么多
"""
file_path = "F:\XuRui\study\论文\实验工具\论文负载\MibenchTrace"

access_sequence = []
count = 0
with open(file_path + "//susan.txt",encoding='gb18030',errors='ignore') as file_object:
    for line in file_object.readlines():
        line = line.replace(' ','').strip()   #去除全部空格
        #print(line)
        if line[16] == '7'and line[17]=='6':
            print("xxx")
            continue
        else:
            count =count+1
            print("#####",count)
            access_sequence.append(line.split(','))
f = open(file_path + "//susan_new.txt",'a')
for i in range(len(access_sequence)):
    s = str(access_sequence[i]).replace('[', '').replace(']', '')
    s = s+'\n'
    f.write(s)
f.close()
print("Success!")