'''
经典算法 SOA
'''

import copy

# 将访问序列构建成一个无向图 key是边，value是边的权重
def construct_graph(access_sequence):
    graph = {}
    for i in range(len(access_sequence) - 1):
        j = i + 1
        key = (access_sequence[i], access_sequence[j])
        key1 = (access_sequence[j], access_sequence[i])
        if key in graph:
            graph[key] = graph[key] + 1
        elif key1 in graph:
            graph[key1] = graph[key1] + 1
        else:
            graph[(access_sequence[i], access_sequence[j])] = 1
    graph0 = copy.deepcopy(graph)
    for i in graph.keys():

        if i[0] == i[1]:
            #print("i", i)
            graph0.pop(i)  # 删除key中两个元素相等的key及值
    #print(len(graph),len(graph0))
    return graph0

# 统计现有的图里每个点的度
def count_degree(V,E):
    degree=[]
    count = 0
    for i in V:
        for j in E:
            if i in j:
                count = count +1
            else:
                continue
        degree.append([i, count])
        count = 0
    return degree

# 判断是否有环
def have_cycle(V,E):
    degree = count_degree(V,E)
    E2 = copy.deepcopy(E)
    i = 0
    while i <len(degree):
        if degree[i][1] == 0:
            degree.remove(degree[i])
            i = 0
        elif degree[i][1] == 1:
            for j in E2:
                if degree[i][0]==j[0]:
                    E2.remove(j)
                    k = 0
                    while k < len(degree):  # 更新节点的度
                        if j[1]==degree[k][0]:
                            degree[k][1]=degree[k][1]-1
                            break
                        else:
                            k = k +1
                            continue
                elif degree[i][0] == j[1]:
                    E2.remove(j)
                    k = 0
                    while k < len(degree):   # 更新节点的度
                        if j[0]==degree[k][0]:
                            degree[k][1]=degree[k][1]-1
                            break
                        else:
                            k = k+1
                            continue
            degree.remove(degree[i])
            i = 0
        else:
            i = i+1
    if len(degree) == 0:
        return True
    else:
        return False




# 判断加入这条边之后会不会让任何一个点的度大于2
def degree_more2(V,E):
    f = True
    for i in V:
        count = 0
        for j in E:
            if i in j:
                count = count + 1
            else:
                continue
        if count>2:
            f = False
            break
    return f

# 将边按照权重降序排序

def sort_edge(graph):
    graph_sorted=sorted(graph.items(),key=lambda kv:(kv[1],kv[0]),reverse= True)
    #print(graph_sorted)
    F = []
    for i in graph_sorted:
        F.append(i[0])
    return F

# 选边
def select_edge(D,graph):
    V1 = copy.deepcopy(D)
    E1 = []
    F = sort_edge(graph)
    while len(E1)<len(V1)-1 and len(F)>0:
        e = F[0]
        F.remove(F[0])
        E1.append(e)
        flag1 = degree_more2(V1,E1)
        if flag1:
            flag2 = have_cycle(V1,E1)
            if flag2:
                continue
            else:
                E1.pop()
        else:
            E1.pop()
    return E1

# 找度为1的点
def degree1(V,E1):
    x = 0
    #E2 = copy.deepcopy(E1)
    for i in V:
        count = 0
        for j in E1:
            if i in j:
                count = count + 1
        if count == 1:
            x = i  # 找到了度为1的点
            break
    return x

# 找到度为1的点在的边，并将其加入顺序中，将该边中的另一个点更新为新的度为0的边
def degree0(x,E1,order):
    #rder = []
    for k in E1:
        if x == k[0]:
            order.append(k[0])
            order.append(k[1])
            x = k[1]
            E1.remove(k)
            break
        elif x == k[1]:
            order.append(k[1])
            order.append(k[0])
            x = k[0]
            E1.remove(k)
            break
    return order,x,E1

def construct_order(V,E1):
    x = degree1(V,E1)
    E2 = copy.deepcopy(E1)
    order = []
    while len(E2)>0:
        i = 0
        #for i in range(len(E2)):
        while i < len(E2):
            if x in E2[i]:
                order,x,E2 = degree0(x,E2,order)
            else:
                i = i+1
                continue
            i = 0
        x = degree1(V,E2)
    return order

def compute_cost(order,access_sequence,Nr,Nw,Tr,Tw,Ts,Er,Ew,Es,Ar):
    port = 0
    shift = 0
    for i in access_sequence:
        shift = shift + abs(order.index(i)-port)
        port = order.index(i)
    T = len(Nr)*Tr+len(Nw)*Tw + shift*Ts
    E = len(Nr)*Er+len(Nw)*Ew + shift*Es
    Area = len(order)*Ar

    return shift,T,E,Area



if __name__ == "__main__":

    # 配置SRAM和RM
    Trr = 3.78
    Twr = 10.23
    Tsr = 4.95  # RM的移动延迟
    Ar = 128/32  # RM存32个数的area
    Err = 337.62  # RM读的energy  单位是pJ
    Erw = 1140  # RM写的energy
    Ers = 328.62  # RM移动操作的energy
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

    #print("Nr:", len(Nr), Nr)
    #print("Nw:", len(Nw), Nw)
    #print("access_sequence", len(access_sequence))

    #data_SRAM = []
    graph1 = construct_graph(access_sequence)
   # print("graph",graph1)
    #graph2 = sort_edge(graph1)
    #print("graph", graph2)
    E0 = select_edge(D,graph1)
    #order = []
    order = construct_order(D,E0)  # order就是placement
    order= list(set(order))
    for i in D:
        if i not in order:
            order.append(i)
    print("access_sequence:",access_sequence)
    print("SOA的Placement为：",order)

    shift,latency,energy,area = compute_cost(order,access_sequence,Nr,Nw,Trr,Twr,Tsr,Err,Erw,Ers,Ar)
    print("SOA的移动次数为：",shift)
    print("SOA的延迟为：",latency)
    print("SOA的能耗为：",energy)
    print("SOA的面积为：",area)

