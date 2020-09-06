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


if __name__ == "__main__":

    # 配置SRAM和RM
    Trr= 3.78
    Twr = 10.23
    Tsr = 4.95    #RM的移动延迟
    Ts = 3.94   #SRAM的延迟
    Ar = 128/32   # RM存32个数的area是128，一个就是2
    As = 120  # SRAM 存一个数的area
    Err =337.62  # RM读的energy  单位是pJ
    Erw = 1140 # RM写的energy
    Ers = 328.62 #RM移动操作的energy
    Es = 226 # SRAM的energy
    fold = round(Twr/Ts,3)  # 一个写相当于几个移动,保留3位小数
    #print("fold",fold)
    data_SRAM = []

    file_path = "D:\XuRui\study\论文\实验工具及负载\负载\Mibench\mibenchTrace"

    rw_sequence = []
    with open(file_path + "//1core_rwnum.txt",encoding='gb18030',errors='ignore')as file:
        for line in file.readlines():
            rw_sequence.append(line.replace(',','').split())
    # print("rw_sequence:",rw_sequence[2][1])
    access_sequence = []
    with open(file_path + "//1core_num.txt",encoding='gb18030',errors='ignore')as file:
        for line in file.readlines():
            access_sequence.extend(line.split())
        access_sequence = list(map(int, access_sequence))


    D = list(set(access_sequence))


    # 统计每个数据被读被写的次数
    Nr = [0 for i in range(len(D)+1)]  # 读的次数
    Nw = [0 for i in range(len(D)+1)]  # 写的次数

    for i in range(len(rw_sequence)):
        if rw_sequence[i][0] == 'R':
            index = access_sequence[i]
            Nr[index] = Nr[index] + 1
        elif rw_sequence[i][0] == 'W':
            index = access_sequence[i]
            Nw[index] = Nw[index] +1

    #print("Nr:",len(Nr),Nr)
    #print("Nw:",len(Nw),Nw)
    #print("access_sequence",len(access_sequence))

    p0,count_s,Ns0 = initial_placement(access_sequence,D)
    cost0 = Trr*sum(Nr) + Twr *sum(Nw) + Tsr*Ns0    # FCFS的总延迟
    energy = Err*sum(Nr) + Erw *sum(Nw) + Ers*Ns0
    area = Ar * len(D)
    # cost0 = compute_cost(Ns0, Nr, Nw, data_SRAM, Trr, Twr, Tsr, Ts, D)

    #print("FCFS的count_s:",len(count_s),count_s)
    print("FCFS的shift次数：",Ns0,"FCFS的延迟：",cost0,"FCFS的能耗：",energy,"FCFS的面积：",area)