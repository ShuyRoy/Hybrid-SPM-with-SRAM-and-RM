"""
将一开始每个benchmark中重复的删掉
"""

file_path = "F:\XuRui\study\论文\实验工具\论文负载\MibenchTrace"

access_sequence = []
access_sequence1=[]
count = 0
with open(file_path + "//bitcount_new1.txt",encoding='gb18030',errors='ignore') as file_object:
    for line in file_object.readlines():
        line = line.replace(' ','').strip()   #去除全部空格
        line = line.replace("'", '')
        #print(line)
        access_sequence.append(line.split(','))
access_sequence.reverse()
print("11111111111111111111")
print(access_sequence)
with open(file_path + "//basicmath_new1.txt",encoding='gb18030',errors='ignore') as file_object:
    # print("scccccccccc")
    for line in file_object.readlines():
        line = line.replace(' ','').strip()   #去除全部空格
        line = line.replace("'", '')
        access_sequence1.append(line.split(','))
access_sequence1.reverse()
print("2222222222222")
count = 0
for i in range(0,len(access_sequence)):
    # print(access_sequence1[i][1])
    if i > len(access_sequence1):
        break
    if access_sequence[i][1] ==access_sequence1[i][1]:
        access_sequence.remove(access_sequence[i])
        access_sequence1.remove(access_sequence1[i])
        count = count+1
        print(count)
    else:
        print("OK!!!!!!")
        break
access_sequence.reverse()
access_sequence1.reverse()
# print(count)
f = open(file_path + "//bitcount_new2.txt",'a')
for i in range(len(access_sequence)):
    s = str(access_sequence[i]).replace('[', '').replace(']', '')
    s = s+'\n'
    f.write(s)
f.close()
print("Success!")
f = open(file_path + "//basicmath_new2.txt",'a')
for i in range(len(access_sequence1)):
    s = str(access_sequence1[i]).replace('[', '').replace(']', '')
    s = s+'\n'
    f.write(s)
f.close()
print(len(access_sequence))
print(len(access_sequence1))
print("Yhea!Success!")
