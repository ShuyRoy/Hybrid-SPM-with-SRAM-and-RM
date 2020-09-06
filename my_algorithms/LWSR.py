"""
自己的算法
将写次数加上假如去掉该数据后会减少的移动的和最大的放大SRAM
且要使用尽量少的SRAM
"""
import copy
import math
import time

def get_key(dict, value):
    return [k for k, v in dict.items() if v == value]


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

# 依次选每次访问该数前需要移动次数最大的一个数放到SRAM上，并更新各个参数
def max_sd(count_s,p,Nw,Nr,fold,access_sequence,rw_sequence,sram_d):
    count_ws = [0 for i in range(len(count_s))] # 记录每个数据2倍的读写加移动次数的列表
    Nw_fold = [0 for i in range(len(count_s))]  # 乘了倍数后的写
    for i in range(len(Nw)):
        if i not in sram_d:
            Nw_fold[i] = Nw[i] * fold
            count_ws[i] = round(Nw_fold[i] + count_s[i],2)
    max_ws = max(count_ws)   # 找出最大值是多少
    # print("写加移动次数统计",max_ws,count_ws)
    # 根据找出的最大值，找出符合这个值的被访问的那些data
    count_s1 = [i for i in range(len(count_ws)) if count_ws[i] == max_ws]

    # 找出上一步选出来移动次数加写次数最大的一组数对应的读次数
    # print("选出移动大的数",count_s1)
    count_r = {}
    for i in range(len(count_s1)):
        count_r[count_s1[i]] = Nr[count_s1[i]]
    # print("选的相同移动加写的数及它们的读次数",count_r)
    # 选出这一组读次数中，读次数最小的那个数
    max_r = min(count_r.values())
    select_d = get_key(count_r,max_r)  # 被选中要被放到SRAM上的数
    select_d1 = select_d[0]    # 上一步选中的数是存在列表中的，这里把它转换成一个单独的数
    # print("选的数及它的读次数",select_d1,max_r)

    # 使用tmp_p表示中间过程的Placement
    tmp_p = copy.deepcopy(p)  # 表示过程中的Placement
    # 更新Placement
    # print("选之前的Placement",len(tmp_p),tmp_p)
    tmp_p.remove(select_d1)
    # print("此时的Placement",len(tmp_p),tmp_p)

    #更新访问序列
    tmp_access = copy.deepcopy(access_sequence)
    while select_d1 in tmp_access:
        tmp_access.remove(select_d1)


    # 更新读写序列
    a = []
    b = []
    for i in rw_sequence:
        a.append(i[0])
        b.append(i[1])
        b = list(map(int,b))
    while select_d1 in b:
        del a[b.index(select_d1)]   # del 可以按照索引删除元素
        b.remove(select_d1)

    tmp_rwsequence = list(zip(a,b))
    # print("tmp_rwsequence", len(tmp_rwsequence),tmp_rwsequence)

    # 更新移动次数
    tmp_counts = [0 for i in range(len(p0)+1)]
    port = 0
    # print("tmp_access",len(tmp_access),len(tmp_counts))
    for i in tmp_access:
        tmp_counts[i] = tmp_counts[i]+abs(tmp_p.index(i)-port)
        port = tmp_p.index(i)


    return select_d1,tmp_p,tmp_counts,sum(tmp_counts),tmp_access,tmp_rwsequence

def compute_shift(sramd,placement,access):
    port = 0
    shift_num = 0
    for i in access:
        if i not in sramd:
            shift_num = shift_num + abs(placement.index(i)-port)
            port = placement.index(i)
    return shift_num

def compute_cost(ns,Nr,Nw,sram_d,Trr,Twr,Tsr,Ts,D):
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
            energy_RM = energy_RM +  Nr[i]*Err + Nw[i]*Erw
    cost = cost_RM + cost_sram
    energy = energy_sram + energy_RM
    return cost,energy



def reduce_sram(sram_d,x,p0,access):
    N_needreduce =math.ceil(len(sram_d) * x)  # 需要减少的个数
    p00 = copy.deepcopy(p0)
    # SramToRm = sram_d[len(sram_d)-N_needreduce+1:] # 需要拿出来放回RM的
    sram_d1 = sram_d[:len(sram_d)-N_needreduce]    # SRAM上剩下的数据

    # 更新此时的Placement
    for i in sram_d1:
        if i in p00:
            p00.remove(i)
    ns=compute_shift(sram_d1, p00, access)   # 得到该情况下的总移动次数
    cost2,energy2= compute_cost(ns, Nr, Nw, sram_d1, Trr, Twr, Tsr, Ts, D)
    # print("%%%%%%%%%%%%%%%%%", p00, sram_d1)
    return cost2,energy2,ns,sram_d1



if __name__ == "__main__":

    # 配置SRAM和RM
    Trr= 3.78
    Twr = 10.23
    Tsr = 4.95    #RM的移动延迟
    Ts = 3.94   #SRAM的延迟
    Ar = 128/32   # RM存32个数的area是128，一个就是2
    As = 120  # SRAM 存一个数的area
    Err =337.62  # RM读的energy  单位是pJ
    Erw = 1140 # RM写的energy单位是pJ
    Ers = 328.62 #RM移动操作的energy单位是pJ
    Es = 226 # SRAM的energy单位是pJ
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

    print("Nr:",len(Nr),Nr)
    print("Nw:",len(Nw),Nw)
    print("access_sequence",len(access_sequence))

    p0,count_s,Ns0 = initial_placement(access_sequence,D)
    cost0 = Trr*sum(Nr) + Twr *sum(Nw) + Tsr*Ns0    # FCFS的总延迟
    energy0 = Err*sum(Nr) + Erw *sum(Nw) + Ers*Ns0
    # cost0 = compute_cost(Ns0, Nr, Nw, data_SRAM, Trr, Twr, Tsr, Ts, D)

    #print("FCFS的count_s:",len(count_s),count_s)
    print("FCFS的cost：",cost0,"FCFS的shift次数：",Ns0,"FCFS的能耗：",energy0)

    N_RM = len(D)    # RM的容量就是数据的多少
    N_SRAM = N_RM//5   # SRAM的容量是RM的1/5
    #N_SRAM = 1000

    # 用一个列表表示选中放在SRAM中的数
    accse=copy.deepcopy(access_sequence)
    rwse =copy.deepcopy(rw_sequence)
    p = p0
    counts = count_s

    aaa = 0
    # 获得一个初始放在SRAM上的数据的集合
    while len(data_SRAM) < N_SRAM:
        #print("$$$$$$$$$$$$$$$$$", aaa + 1)
        select_data,tmp_p,tmp_counts,Ns1,tmp_access,tmp_rwsequence = max_sd(counts, p, Nw, Nr, fold,accse,rwse,data_SRAM)
        #print("$$$$$$$$$$$$$$$$$", aaa + 1)
        p = tmp_p
        counts = tmp_counts
        accse = tmp_access
        rwse = tmp_rwsequence
        data_SRAM.append(select_data)

    cost1,energy1=compute_cost(Ns1, Nr, Nw, data_SRAM, Trr, Twr, Tsr, Ts, D)  # 使用全部SRAM时的cost
    area1 = As * len(data_SRAM) + Ar +(len(D)-len(data_SRAM))
    # print("cost",cost1)

    # 最开始减少的cost和移动的百分比
    initial_cost_reduce = round(abs(cost0-cost1)/cost0,2)
    initial_shift_reduce = round(abs(Ns0-Ns1)/Ns0,2)
    # print(Ns1,cost1)
    # 调整比例
    diff_cost = 0.2   # 最终优化的和初始优化的cost的差值希望不超过20%
    diff_shift = 0.2   # 最终优化的和初始优化的shift的差值希望不超过15%
    x = 0.3  # 每次减少SRAM上x的数据
    # my_break = 0.0001   # 梯度下降中可以忍受的误差
    cost_reduce = initial_cost_reduce
    shift_reduce = initial_shift_reduce
    print("SRAM上的数：",data_SRAM)
    print("SRAM全部使用cost减少的百分比",initial_cost_reduce,"SRAM全部使用shift减少的百分比",initial_cost_reduce,"SRAM全部使用cost",cost1,"SRAM全部使用shift",Ns1,"SRAM上的数据量",len(data_SRAM))
    print("SRAM全部使用能耗",energy1,"SRAM全部使用面积",area1)

    data_SRAM2 = copy.deepcopy(data_SRAM)
    time_start = time.time()
    while initial_cost_reduce - cost_reduce < diff_cost and initial_shift_reduce - shift_reduce < diff_shift:
        # print("****",len(access_sequence))
        cost2,energy2, Ns2, data_SRAM2 = reduce_sram(data_SRAM2, x, p0, access_sequence)
        cost_reduce = round(abs(cost0 - cost2) / cost0, 2)
        shift_reduce = round(abs(Ns0 - Ns2) / Ns0, 2)
        area = len(data_SRAM2)*As + (len(D) - len(data_SRAM2))*Ar
        print("cost减少的百分比：", cost_reduce, "shift减少的百分比：", shift_reduce, "延迟：", cost2, "移动次数：", Ns2, "SRAM上数据量：",
              len(data_SRAM2),"能耗",energy2,"总面积", area)
        # if initial_cost_reduce - cost_reduce < diff_cost and initial_shift_reduce - shift_reduce < diff_shift:
        #         #     continue
        #         # else:
        #         #     print("最后一组不满足条件")
        #         #     break
    time_end = time.time()
    print("time cost",time_end-time_start)


    # data_SRAM1 = copy.deepcopy(data_SRAM2)
    # data_SRAM2 = []
    # while abs(len(data_SRAM1)-len(data_SRAM2)) > 5:
    #     # print("88888888888888")
    #     print("x", x)
    #     data_SRAM2=copy.deepcopy(data_SRAM)
    #     cost_reduce = initial_cost_reduce
    #     shift_reduce = initial_shift_reduce
    #     data_SRAM1 = copy.deepcopy(data_SRAM2)
    #     while initial_cost_reduce-cost_reduce<diff_cost and initial_shift_reduce - shift_reduce<diff_shift:
    #         # print("****",len(access_sequence))
    #         cost2,Ns2,data_SRAM2=reduce_sram(data_SRAM2, x, p0, access_sequence)
    #         cost_reduce = round(abs(cost0-cost2)/cost0,2)
    #         shift_reduce = round(abs(Ns0-Ns2)/Ns0,2)
    #         print("cost减少的百分比：",cost_reduce,"shift减少的百分比：", shift_reduce,"cost：",cost2,"shift：",Ns2,"SRAM上数据量：",len(data_SRAM2))
    #     x = round(x * (1-0.05),2)

