"""
对Intel pin拿到的trace进行数据格式的处理
"""

file_path = "D:\XuRui\study\论文\实验工具及负载\负载\Mibench\mibenchTrace"

a = []
b = []
# count = 0
with open(file_path + "//dijkstra_small.txt",encoding='gb18030',errors='ignore') as file_object:
    for line in file_object.readlines():
        line = line.replace(' ','').strip()   #去除全部空格
        # print(line)
        a.append(line[9])  #读写列表
        b.append(line[10:])   #访问地址列表
        # count = count +1
        # print(a)
        # print(b)
# 将地址转换成数字
# count = 0
buf = []
b_num = []
buf.append('ccccc')   #这样比的时候就可以从1开始了。
for i in b:
    if i in buf:
        count= buf.index(i)
        b_num.append(count)
    else:
        buf.append(i)
        count = buf.index(i)
        b_num.append(count)
#print(b_num)
#print(len(b_num),len(b))

c = list(zip(a,b_num))  #将两个一维列表合成一个二维列表

#print(c)
#print(max(b))


f = open(file_path + "//dijkstra_small_rwnum.txt",'a')
for i in range(len(c)):
    s = str(c[i]).replace('[', '').replace('(','').replace("'",'').replace(')','').replace(']', '')
    s = s+'\n'
    f.write(s)
f.close()

f = open(file_path + "//dijkstra_small_num.txt",'a')
for i in range(len(b_num)):
    s = str(b_num[i]).replace('[', '').replace(']', '')
    s = s+'\n'
    f.write(s)
f.close()