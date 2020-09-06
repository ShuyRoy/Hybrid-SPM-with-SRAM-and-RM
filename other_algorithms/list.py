"""
给定访问序列，对数据进行顺序放置。
2个r/w port
"""

def list_place(access_sequence,data,domain):
    a = 0 # 用来标记现在指向RM的那个位置处
    for i in access_sequence:
        if i in data and i not in domain:
            domain[a] = i  # 将现在所访问的数据放置
            a = a + 1
        if i in domain:
            continue
    return domain

def RM_acc_performance(access_sequence,acc_l,acc_e):
    sum_acc_latency = len(access_sequence) * acc_l

    sum_acc_energy = len(access_sequence) * acc_e

    return sum_acc_latency,sum_acc_energy

def RM_shift_performance(access_sequence,s_l,s_e,domain,p1,p2,pm):
    count_shift = 0
    for i in access_sequence:
        p = domain.index(i)
        if p < pm :
            count_shift = count_shift + abs(p-p1)
            p1 = p # 将port1移动到p位置处
            p2 = p + pm # 将port2移动到p对应的另一半位置处
            print("a - > b",count_shift)
        else:
            count_shift = count_shift + abs(p-p2)
            p2 = p
            p1 = p - pm



    sum_shift_latency = count_shift * s_l

    sum_shift_energy = count_shift * s_e

    return count_shift,sum_shift_latency,sum_shift_energy



if __name__ == "__main__":

    # 配置RM
    port = 2  # 2 r/w ports
    RM_size = 32  # RM size is 32GB
    domain = [-1 for i in range(0,RM_size)]  # the num of the domain is same as RM_size
    p1 = 0  # initial place of port1
    p2 = RM_size // port + 1 # initial place of port2
    pm = RM_size // port + 1 # middle place of domain
    acc_l = 6.3  # DW-RM access latency
    # w_l = 6.3  # DW-RM write latency
    acc_e = 0.27   # DW-RM access energy
    # w_e = 0.27   # DW-RM write energy
    s_l = 5.87   # DW-RM shift latency
    s_e = 0.45    # DW-RM shift energy


    file_path = "D:\XuRui\study\论文\混合内存\论文\算法实现\exp-1-puremacro//ex1"

    access_sequence = []
    # 读取访问序列
    with open(file_path + "//DataA.txt") as file_object:
        for line in file_object:
            access_sequence.extend(line.rsplit())

        access_sequence = list(map(int, access_sequence))



    # 每个访问序列所访问的数据去重
    #data = []

    data = list(set(access_sequence))
    # print(data.index(0))

    print("访问序列",access_sequence)
    print("访问的所有变量",data)
    print("空的RM",len(domain),domain)
    print("RM上数据放置结果",len(list_place(access_sequence,data,domain)),list_place(access_sequence,data,domain))
    print("RM访问延迟与能耗",RM_acc_performance(access_sequence,acc_l,acc_e))
    print("RM总的移动次数、延迟、能耗", RM_shift_performance(access_sequence,s_l,s_e,domain,p1,p2,pm))


