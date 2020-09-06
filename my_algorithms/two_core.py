"""
2_core，将两个应用的trace合并，模拟2个core拿到的trace，两个core会轮流从SPM中取数据
"""
import random

file_path = "D:\XuRui\study\论文\实验工具及负载\负载\Mibench\mibenchTrace"

# 第一个应用的trace，使用CRC32的，最大为1165，所以之后第二个应用的数据的空间地址要从1166开始
rw_sequence1 = []
with open(file_path + "//2cores_rwnum.txt", encoding='gb18030', errors='ignore')as file:
    for line in file.readlines():
        rw_sequence1.append(line.replace(',', '').split())
print("rw_sequence1:",rw_sequence1)
access_sequence1 = []
with open(file_path + "//2cores_num.txt", encoding='gb18030', errors='ignore')as file:
    for line in file.readlines():
        access_sequence1.extend(line.split())
    access_sequence1 = list(map(int, access_sequence1))

# 第二个应用的trace，使用bitcount的，要将该trace中的每个数都加上1165，表示它的起始地址空间是1166
rw_sequence2 = []
with open(file_path + "//2cores2_rwnum.txt", encoding='gb18030', errors='ignore')as file:
    for line in file.readlines():
        rw_sequence2.append(line.replace(',', '').split())
    for i in rw_sequence2:
        i[1]= int(i[1]) + 1165
print("rw_sequence2:", rw_sequence2)
access_sequence2 = []
with open(file_path + "//2cores2_num.txt", encoding='gb18030', errors='ignore')as file:
    for line in file.readlines():
        access_sequence2.extend(line.split())
    access_sequence2 = list(map(int, access_sequence2))
    for i in range(len(access_sequence2)):
        access_sequence2[i] = access_sequence2[i] + 1165
print(access_sequence2)

# 将两个trace的列表合为一个trace，采用随机的间隔进行合并，每次随机产生一个0~5之间的数进行合并
access_sequence = []
rw_sequence = []
i = 0
while i< len(access_sequence1):
    gap = random.randint(1,5)
    if i+gap>=len(access_sequence1):
        access_sequence.extend(access_sequence1[i:])
        rw_sequence.extend(rw_sequence1[i:])
        access_sequence.extend(access_sequence2[i:i + gap])
        rw_sequence.extend(rw_sequence2[i:i + gap])
    else:
        access_sequence.extend(access_sequence1[i:i + gap])
        rw_sequence.extend(rw_sequence1[i:i + gap])
        access_sequence.extend(access_sequence2[i:i + gap])
        rw_sequence.extend(rw_sequence2[i:i + gap])
    i=i+gap
print("1的长度",len(access_sequence1),"2的长度：",len(access_sequence2),"总的长度：",len(access_sequence))
access_sequence.extend(access_sequence2[len(access_sequence1):])
rw_sequence.extend(rw_sequence2[len(rw_sequence1):])

print("1的长度",len(access_sequence1),"2的长度：",len(access_sequence2),"总的长度：",len(access_sequence),len(rw_sequence))

f = open(file_path + "//4cores2_rwnum.txt",'a')
for i in range(len(rw_sequence)):
    s = str(rw_sequence[i]).replace('[', '').replace('(','').replace("'",'').replace(')','').replace(']', '')
    s = s+'\n'
    f.write(s)
f.close()

f = open(file_path + "//4cores2_num.txt",'a')
for i in range(len(access_sequence)):
    s = str(access_sequence[i]).replace('[', '').replace(']', '')
    s = s+'\n'
    f.write(s)
f.close()