"""
设置阈值将写次数多的放到SRAM上
"""
import copy


# 根据FCFS产生一个初始的Placement,同时获得了访问每个数需要移动的次数。
def initial_placement(access_sequence,D):
    p0 = []   # 用来表示初始的Placement
    port = 0    # 表示当前port的位置
    count_s = [0 for i in range(len(D)+1)]   # 统计每个数据被访问前需要移动的总次数
    for i in access_sequence:
        if i in p0:
            count_s[i] = count_s[i] + abs(p0.index(i)-port)
            port = p0.index(i)
        elif i not in p0:
            p0.append(i)
            count_s[i] = count_s[i] + abs(p0.index(i)-port)
            port = p0.index(i)
    return p0,count_s,sum(count_s)


def compute_shift(sramd,placement,access):
    port = 0
    shift_num = 0
    for i in access:
        if i not in sramd:
            shift_num = shift_num + abs(placement.index(i)-port)
            port = placement.index(i)
    return shift_num

def compute_cost(ns,Nr,Nw,sram_d,Trr,Twr,Tsr,Ts,D,Ers,Erw,Es,Err):
    cost_sram = 0
    energy_sram = 0
    cost_RM = ns * Tsr
    energy_RM = ns * Ers
    # SRAM上的读写延迟
    for i in sram_d:
        cost_sram = cost_sram+(Nr[i]+Nw[i])*Ts
        energy_sram = energy_sram + (Nr[i]+Nw[i])*Es
    # RM上的读写延迟加移动延迟
    for i in D:
        if i not in sram_d:
            cost_RM = cost_RM + Nr[i]*Trr + Nw[i]*Twr
            energy_RM = energy_RM + Nr[i]*Err + Nw[i]*Erw
    cost = cost_RM + cost_sram
    energy = energy_RM + energy_sram

    return cost,energy

if __name__ == "__main__":

    # 配置SRAM和RM
    Trr = 3.78
    Twr = 10.23
    Tsr = 4.95  # RM的移动延迟
    Ts = 3.94  # SRAM的延迟
    Ar = 128 / 32  # RM存32个数的area是128，一个就是2
    As = 120  # SRAM 存一个数的area
    Err = 337.62  # RM读的energy  单位是pJ
    Erw = 1140  # RM写的energy单位是pJ
    Ers = 328.62  # RM移动操作的energy单位是pJ
    Es = 226  # SRAM的energy单位是pJ
    # fold = round(Twr / Ts, 3)  # 一个写相当于几个移动,保留3位小数
    # print("fold", fold)
    num_data_SRAM = 684 # 放根据LWSR得到放多少数据放在SRAM上

    file_path = "D:\XuRui\study\论文\实验工具及负载\负载\Mibench\mibenchTrace"

    rw_sequence = []
    with open(file_path + "//1core_rwnum.txt", encoding='gb18030', errors='ignore')as file:
        for line in file.readlines():
            rw_sequence.append(line.replace(',', '').split())
    # print("rw_sequence:",rw_sequence[2][1])
    access_sequence = []
    with open(file_path + "//1core_num.txt", encoding='gb18030', errors='ignore')as file:
        for line in file.readlines():
            access_sequence.extend(line.split())
        access_sequence = list(map(int, access_sequence))

    D = list(set(access_sequence))

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

    print("Nr:", len(Nr), Nr)
    print("Nw:", len(Nw), Nw)
    print("access_sequence", len(access_sequence))

    data_SRAM = []
    Nw1 = copy.deepcopy(Nw)
    for i in range(num_data_SRAM):
        data_SRAM.append(Nw1.index(max(Nw1)))
        Nw1[Nw1.index(max(Nw1))]=0

    p0, count_s, Ns0 = initial_placement(access_sequence, D)
    cost0 = Trr * sum(Nr) + Twr * sum(Nw) + Tsr * Ns0  # FCFS的总延迟

    # count_s1 = copy.deepcopy(count_s)
    # for i in range(num_data_SRAM):
    #     data_SRAM.append(count_s1.index(max(count_s1)))
    #     count_s1.remove(max(count_s1))

    Ns1 = compute_shift(data_SRAM, p0, access_sequence)
    cost1,energy = compute_cost(Ns1, Nr, Nw, data_SRAM, Trr, Twr, Tsr, Ts, D,Ers,Erw,Es,Err)

    cost_reduce = round(abs(cost0-cost1)/cost0,2)
    shift_reduce = round(abs(Ns0-Ns1)/Ns0,2)

    area = Ar * (len(D)-len(data_SRAM))+As*len(data_SRAM)
    print(data_SRAM)
    print("WA的cost减少的百分比",cost_reduce,"WA的shift减少的百分比",shift_reduce,"WA的延迟",cost1,"WA的shift",Ns1)
    print("WA的能耗为：",energy,"WA的面积为：",area)