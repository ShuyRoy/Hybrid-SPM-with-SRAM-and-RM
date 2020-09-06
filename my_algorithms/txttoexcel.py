
from xlwt import *
from openpyxl import  Workbook
# import pandas as pd

file_path = "F:\XuRui\study\论文\实验工具\论文负载\MibenchTrace"

"""
将txt中的内容转换成字典
"""
# access_sequence = {}
#a =[]
# with open(file_path + "//test.txt",encoding='gb18030',errors='ignore') as file_object:
#     for line in file_object.readlines():
#         line = line.replace(' ','').strip()   #去除全部空格
#         #print(line)
#         a.extend(line.split(','))
#         k = a[0]
#         #print(k)
#         for v in a:
#             if a.index(v)>0 and a.index(v)<3:
#                 access_sequence.setdefault(k,[]).append(v)
#         a =[]
#
# print(access_sequence)
"""
将字典存到Excel中，未完成
"""

# file = Workbook(encoding='utf-8')
#
# table = file.add_sheet('test')
#
# ldata =[]
# num = [b for b in access_sequence] #将所有的key取出来
#
# for x in num:
#     t = []

"""
将txt处理成列表，再将列表存到Excel中
"""
access_sequence = []
access_sequence1=[]
count = 0
with open(file_path + "//bitcount_new.txt",encoding='gb18030',errors='ignore') as file_object:
    for line in file_object.readlines():
        line = line.replace(' ','').strip()   #去除全部空格
        #print(line)
        access_sequence.append(line.split(','))

print("11111111111111111111")
print(access_sequence)
with open(file_path + "//basicmath_new.txt",encoding='gb18030',errors='ignore') as file_object:
    print("scccccccccc")
    for line in file_object.readlines():
        line = line.replace(' ','').strip()   #去除全部空格
        access_sequence1.append(line.split(','))
print("2222222222222")
count = 0
for i in range(0,len(access_sequence)):
    print(access_sequence1[i][1])
    if i > len(access_sequence1):
        break
    if access_sequence[i][1] ==access_sequence1[i][1]:
        count = count+1
        print(count)
    else:
        print("OK!!!!!!")
        break

print(count)
# f = Workbook()
# sheet=f.active

# sheet.append()
# sheet = f.add_sheet("sheet1",cell_overwrite_ok=True)

# for i in range(0,len(access_sequence)):
#     for j in range(0,len(access_sequence[i])):
#         sheet.write(i,j,access_sequence[i][j])

# for i in range(0,len(access_sequence)):
#     sheet.append(access_sequence[i])
# f.save(file_path+"//test.xls")

print("Success!")