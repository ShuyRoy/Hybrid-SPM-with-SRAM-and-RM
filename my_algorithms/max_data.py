file_path = "D:\XuRui\study\论文\实验工具及负载\负载\Mibench\mibenchTrace"

# rw_sequence = []
# with open(file_path + "//ex_rwnum.txt", encoding='gb18030', errors='ignore')as file:
#     for line in file.readlines():
#         rw_sequence.append(line.replace(',', '').split())
# print("rw_sequence:",rw_sequence[2][1])
access_sequence = []
with open(file_path + "//2cores_num.txt", encoding='gb18030', errors='ignore')as file:
    for line in file.readlines():
        access_sequence.extend(line.split())
    access_sequence = list(map(int, access_sequence))

D = list(set(access_sequence))

print(max(D))