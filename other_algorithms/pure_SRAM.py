"""
纯SRAM时候的开销
"""

def compute_cost(Ts,As,Es,access_sequence,D):
    T = len(access_sequence)* Ts
    E = len(access_sequence)*Es
    A = len(D)*As

    return T,E,A

if __name__ == "__main__":

    # 配置SRAM和RM
    Ts = 3.94  # SRAM的延迟
    As = 120  # SRAM 存一个数的area
    Es = 226  # SRAM的energy
    # fold = round(Twr / Ts, 3)  # 一个写相当于几个移动,保留3位小数
    # print("fold", fold)
    #num_data_SRAM = 228  # 放根据LWSR得到放多少数据放在SRAM上

    file_path = "D:\XuRui\study\论文\实验工具及负载\负载\Mibench\mibenchTrace"

    rw_sequence = []
    with open(file_path + "//2cores_rwnum.txt", encoding='gb18030', errors='ignore')as file:
        for line in file.readlines():
            rw_sequence.append(line.replace(',', '').split())
    # print("rw_sequence:",rw_sequence[2][1])
    access_sequence = []
    with open(file_path + "//2cores_num.txt", encoding='gb18030', errors='ignore')as file:
        for line in file.readlines():
            access_sequence.extend(line.split())
        access_sequence = list(map(int, access_sequence))

    D = list(set(access_sequence))  #  data

    # 统计每个数据被读被写的次数
    Nr = [0 for i in range(len(D) + 1)]  # 读的次数
    Nw = [0 for i in range(len(D) + 1)]  # 写的次数

    for i in range(len(rw_sequence)):
        if rw_sequence[i][0] == 'R':
            index = access_sequence[i]
            Nr[index] = Nr[index] + 1
        elif rw_sequence[i][0] == 'W':
            index = access_sequence[i]
            Nw[index] = Nw[index] + 1

    latency,energy,area = compute_cost(Ts,As,Es,access_sequence,D)
    print("纯SRAM的延迟为：",latency)
    print("纯SRAM的能耗为：",energy)
    print("纯SRAM的面积为：",area)
