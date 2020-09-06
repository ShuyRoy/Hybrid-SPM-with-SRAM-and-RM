"""
4_core，将四个应用的trace合并，模拟4个core拿到的trace，四个core会轮流从SPM中取数据
"""
import random

file_path = "D:\XuRui\study\论文\实验工具及负载\负载\Mibench\mibenchTrace"

# 第一个应用的trace，使用CRC32的，最大为1165，所以之后第二个应用的数据的空间地址要从1166开始
rw_sequence1 = []
with open(file_path + "//CRC32_rwnum.txt", encoding='gb18030', errors='ignore')as file:
    for line in file.readlines():
        rw_sequence1.append(line.replace(',', '').split())
#print("rw_sequence1:",rw_sequence1)
access_sequence1 = []
with open(file_path + "//CRC32_num.txt", encoding='gb18030', errors='ignore')as file:
    for line in file.readlines():
        access_sequence1.extend(line.split())
    access_sequence1 = list(map(int, access_sequence1))

# 第二个应用的trace，使用bitcount的，要将该trace中的每个数都加上1165，表示它的起始地址空间是1166
rw_sequence2 = []
with open(file_path + "//bitcount_rwnum.txt", encoding='gb18030', errors='ignore')as file:
    for line in file.readlines():
        rw_sequence2.append(line.replace(',', '').split())
    for i in rw_sequence2:
        i[1]= int(i[1]) + 1165
#print("rw_sequence2:", rw_sequence2)
access_sequence2 = []
with open(file_path + "//bitcount_num.txt", encoding='gb18030', errors='ignore')as file:
    for line in file.readlines():
        access_sequence2.extend(line.split())
    access_sequence2 = list(map(int, access_sequence2))
    for i in range(len(access_sequence2)):
        access_sequence2[i] = access_sequence2[i] + 1165
#print(access_sequence2)


# 第三个应用的trace，使用qsort的，要将该trace中的每个数都加上1165+1190=2355，表示它的起始地址空间是2356
rw_sequence3 = []
with open(file_path + "//qsort_rwnum.txt", encoding='gb18030', errors='ignore')as file:
    for line in file.readlines():
        rw_sequence3.append(line.replace(',', '').split())
    for i in rw_sequence3:
        i[1]= int(i[1]) + 2355
#print("rw_sequence3:", rw_sequence3,len(rw_sequence3))
access_sequence3 = []
with open(file_path + "//qsort_num.txt", encoding='gb18030', errors='ignore')as file:
    for line in file.readlines():
        access_sequence3.extend(line.split())
    access_sequence3 = list(map(int, access_sequence3))
    for i in range(len(access_sequence3)):
        access_sequence3[i] = access_sequence3[i] + 2355
#print(access_sequence3,len(access_sequence3),max(access_sequence3))



# 第四个应用的trace，使用blowfish的，要将该trace中的每个数都加上2355+1216=3571，表示它的起始地址空间是3572
rw_sequence4 = []
with open(file_path + "//blowfish_rwnum.txt", encoding='gb18030', errors='ignore')as file:
    for line in file.readlines():
        rw_sequence4.append(line.replace(',', '').split())
    for i in rw_sequence4:
        i[1]= int(i[1]) + 3571
#print("rw_sequence4:", rw_sequence4)
access_sequence4 = []
with open(file_path + "//blowfish_num.txt", encoding='gb18030', errors='ignore')as file:
    for line in file.readlines():
        access_sequence4.extend(line.split())
    access_sequence4 = list(map(int, access_sequence4))
    for i in range(len(access_sequence4)):
        access_sequence4[i] = access_sequence4[i] + 3571
print(access_sequence4,len(access_sequence4),max(access_sequence4))



# 将四个trace的列表合为一个trace，采用随机的间隔进行合并，每次随机产生一个0~5之间的数进行合并
access_sequence = []
rw_sequence = []
i = 0
while i< len(access_sequence1):
    gap = random.randint(1,5)
    if i+gap >= len(access_sequence1):
        access_sequence.extend(access_sequence1[i:])
        rw_sequence.extend(rw_sequence1[i:])
        access_sequence.extend(access_sequence2[i:i + gap])
        rw_sequence.extend(rw_sequence2[i:i + gap])
        access_sequence.extend(access_sequence3[i:i + gap])
        rw_sequence.extend(rw_sequence3[i:i + gap])
        access_sequence.extend(access_sequence4[i:i + gap])
        rw_sequence.extend(rw_sequence4[i:i + gap])
    else:
        access_sequence.extend(access_sequence1[i:i + gap])
        rw_sequence.extend(rw_sequence1[i:i + gap])
        access_sequence.extend(access_sequence2[i:i + gap])
        rw_sequence.extend(rw_sequence2[i:i + gap])
        access_sequence.extend(access_sequence3[i:i + gap])
        rw_sequence.extend(rw_sequence3[i:i + gap])
        access_sequence.extend(access_sequence4[i:i + gap])
        rw_sequence.extend(rw_sequence4[i:i + gap])

    i=i+gap

j = len(access_sequence1)
i = 0
while i < len(access_sequence2[len(access_sequence1):]):
    gap = random.randint(1, 5)
    if i+j+gap>=len(access_sequence2):
        access_sequence.extend(access_sequence2[i + j:])
        rw_sequence.extend(rw_sequence2[i + j:])
        access_sequence.extend(access_sequence3[i + j:i + j + gap])
        rw_sequence.extend(rw_sequence3[i + j:i + j + gap])
        access_sequence.extend(access_sequence4[i + j:i + j + gap])
        rw_sequence.extend(rw_sequence4[i + j:i + j + gap])
    else:
        access_sequence.extend(access_sequence2[i + j:i + j + gap])
        rw_sequence.extend(rw_sequence2[i + j:i + j + gap])
        access_sequence.extend(access_sequence3[i + j:i + j + gap])
        rw_sequence.extend(rw_sequence3[i + j:i + j + gap])
        access_sequence.extend(access_sequence4[i + j:i + j + gap])
        rw_sequence.extend(rw_sequence4[i + j:i + j + gap])
    # if i < len(access_sequence2[len(access_sequence1):]) and i + gap >= len(access_sequence2[len(access_sequence1):]):
    #     access_sequence.extend(access_sequence2[i + j:len(access_sequence2)])
    #     rw_sequence.extend(rw_sequence2[i + j:len(access_sequence2)])
    #     access_sequence.extend(access_sequence3[i + j:len(access_sequence2)])
    #     rw_sequence.extend(rw_sequence3[i + j:len(access_sequence2)])
    #     access_sequence.extend(access_sequence4[i + j:len(access_sequence2)])
    #     rw_sequence.extend(rw_sequence4[i + j:len(access_sequence2)])
    #     break
    # else:
    i = i + gap

k = len(access_sequence2)
i = 0
while i < len(access_sequence3[len(access_sequence2):]):
    gap = random.randint(1, 5)
    if i+k+gap < len(access_sequence3):
        access_sequence.extend(access_sequence3[i + k:i + k + gap])
        rw_sequence.extend(rw_sequence3[i + k:i + k + gap])
        access_sequence.extend(access_sequence4[i + k:i + k + gap])
        rw_sequence.extend(rw_sequence4[i + k:i + k + gap])
    else:
        access_sequence.extend(access_sequence3[i + k:])
        rw_sequence.extend(rw_sequence3[i + k:])
        access_sequence.extend(access_sequence4[i + k:i + k + gap])
        rw_sequence.extend(rw_sequence4[i + k:i + k + gap])


    # if i < len(access_sequence3[len(access_sequence2):]) and i + gap >= len(access_sequence3[len(access_sequence2):]):
    #     access_sequence.extend(access_sequence3[i + j:len(access_sequence3)])
    #     rw_sequence.extend(rw_sequence3[i + j:len(access_sequence3)])
    #     access_sequence.extend(access_sequence4[i + j:len(access_sequence3)])
    #     rw_sequence.extend(rw_sequence4[i + j:len(access_sequence3)])
    #     break
    # else:
    i = i + gap

#print("1的长度",len(access_sequence1),"2的长度：",len(access_sequence2),"总的长度：",len(access_sequence))
access_sequence.extend(access_sequence4[len(access_sequence3):])
rw_sequence.extend(rw_sequence4[len(rw_sequence3):])

print("1的长度",len(access_sequence1),"2的长度：",len(access_sequence2),"3的长度",len(access_sequence3),"4的长度：",len(access_sequence4),"总的长度：",len(access_sequence),len(rw_sequence))

f = open(file_path + "//4cores_rwnum.txt",'a')
for i in range(len(rw_sequence)):
    s = str(rw_sequence[i]).replace('[', '').replace('(','').replace("'",'').replace(')','').replace(']', '')
    s = s+'\n'
    f.write(s)
f.close()

f = open(file_path + "//4cores_num.txt",'a')
for i in range(len(access_sequence)):
    s = str(access_sequence[i]).replace('[', '').replace(']', '')
    s = s+'\n'
    f.write(s)
f.close()