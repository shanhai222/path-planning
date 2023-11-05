import pandas as pd
import numpy as np
import gol
import re
import pickle
import A_star
import Node

# 生成随机速度
def randfloat(num, l, h):
    if l > h:
        return None
    else:
        a = h - l
        b = h - a
        out = (np.random.rand(num) * a + b).tolist()
        out = np.array(out)
        return out

#计算路段当下所需时间(h)
def calculate_time(length, velocity):
    road_time = np.zeros((1448, 2))
    for i in range(0, 1448):
        road_time[i][0] = length[i][0]
        road_time[i][1] = length[i][1] / velocity[i][1]

    return road_time

#通过坐标判断起始路段
#def start_road():


if __name__ == '__main__':
    gol._init()
    adj_matrix = pd.read_pickle('./data_use/adj_matrix.pkl')  # 路段间的邻接矩阵（有向）
    road_length = pd.read_pickle('./data_use/road_filtered_length.pkl')  # 每个路段的长度
    road_id = pd.read_pickle('./data_use/road_linkid.pkl')  # 路段对应的id
    road_dis = pd.read_pickle('./data_use/dis_mat.pkl')  # 路段间的直线距离
    gol.set_value('adj_matrix', adj_matrix)
    gol.set_value('road_length', road_length)
    gol.set_value('road_id', road_id)
    gol.set_value('road_dis', road_dis)
    #print(length.shape)
    print(road_id[1000])

    # 构造变化前后的速度
    v1 = randfloat(1448, 0, 60)
    v2 = randfloat(1448, 0, 60)
    velocity1 = np.zeros((1448, 2))
    velocity2 = np.zeros((1448, 2))
    for i in range(0, 1448):
        velocity1[i][0] = road_id[i]
        velocity2[i][0] = road_id[i]
        velocity1[i][1] = v1[i]
        velocity2[i][1] = v2[i]

    # 计算变化前后各路段所需时间
    time1 = calculate_time(road_length, velocity1)
    time2 = calculate_time(road_length, velocity2)
    gol.set_value('time_before', time1)
    gol.set_value('time_after', time2)

    start_node = Node.Node(1525982951)
    end_node = Node.Node(1569718849)
    a = A_star.A_star(start_node, end_node)
    if a.start():
        find_ways = gol.get_value('find_ways')
        for i in find_ways:
            print(i)