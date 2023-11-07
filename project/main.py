import pandas as pd
import numpy as np
import torch
import random
import gol
import A_star
import Node
import road_id_hash

#计算路段当下所需时间(h)
def calculate_time(length, velocity):
    road_time = np.zeros((2307, 1))
    for i in range(0, 2307):
        road_time[i][0] = length[i][0] / velocity[i]

    return road_time

#通过坐标判断起始路段
#def start_road():


if __name__ == '__main__':
    gol._init()
    # 路段信息读取
    adj_matrix = pd.read_pickle('./data_use/adj_matrix_filtered_strong.pkl')  # 路段间的邻接矩阵（有向）
    road_length = pd.read_pickle('./data_use/road_filtered_length.pkl')  # 每个路段的长度
    road_id = pd.read_pickle('./data_use/road_network_linkid_filtered.pkl')  # 路段对应的id
    road_dis = pd.read_pickle('./data_use/dis_mat.pkl')  # 路段间的直线距离

    # 将路段id映射为index存储为字典
    road_id_mapping = road_id_hash.road_id_map(road_id)

    gol.set_value('adj_matrix', adj_matrix)
    gol.set_value('road_length', road_length)
    gol.set_value('road_id', road_id)
    gol.set_value('road_dis', road_dis)
    gol.set_value('road_id_mapping', road_id_mapping)
    #print(length.shape)
    # print(road_id[1000])

    # 获取交通状况
    test = pd.read_pickle('./data_use/test.pkl')
    output = torch.load('./data_use/output.pth')  # 预测结果 (870, 1, 1448, 1)

    # 取第i个时间片
    i = random.randint(0, 870)
    #print(i)
    # 当前时间的实时路况
    now_v = test['x'][i][0]  # (1448,1)
    gol.set_value('velocity_now', now_v)
    # 模型预测的下一个时间片的路况
    predict_v = output[i][0].numpy()  # (1448,1) km/h

    # 计算变化前后各路段所需时间
    time1 = calculate_time(road_length, now_v)
    time2 = calculate_time(road_length, predict_v)
    gol.set_value('time_before', time1)
    gol.set_value('time_after', time2)

    start_node = Node.Node(1561692353)
    end_node = Node.Node(1526020425)
    a = A_star.A_star(start_node, end_node)
    if a.start():
        #find_way = gol.get_value('find_way')
        #print(find_way)
        print('find a way successfully!')
        a.path()
    else:
        print('can not find a way!')