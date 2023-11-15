import pandas as pd
import numpy as np
import torch
import random
import gol
import A_star_contrast
import Node
import road_id_hash

#计算路段当下所需时间(h)
def calculate_time(length, velocity):
    road_time = np.zeros((6392, 1))
    for i in range(0, 6392):
        road_time[i][0] = length[i].values[0] / velocity[i]

    return road_time

#通过坐标判断起始路段
# def start_road(gps):

if __name__ == '__main__':
    gol._init()
    # 路段信息读取
    adj_matrix = pd.read_pickle('./data_use/adj_matrix_filtered_6392.pkl')  # 路段间的邻接矩阵（有向）
    road_length = pd.read_pickle('./data_use/road_filtered_length_6392.pkl')  # 每个路段的长度
    #print(road_length[0])
    road_id = pd.read_pickle('./data_use/road_network_linkid_filtered_6392.pkl')  # 路段对应的id
    road_dis = pd.read_pickle('./data_use/dis_mat_6392.pkl')  # 路段间的直线距离

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
    test = pd.read_pickle('./data_use/test_all.pkl')
    output = torch.load('./data_use/output_all.pth')  # 预测结果 (5795, 1, 6392, 1)
    #print(output.shape)
    # 随机取一个时间片作为出发时间
    # now_t = random.randint(0, 5795)
    now_t = 2990  #T0
    # print(i)
    # 当前时间的实时路况
    now_v = test['x'][now_t][0]  # (6392,1)
    #print(now_v)
    gol.set_value('velocity_now', now_v)
    # 模型预测的下一个时间片的路况
    # now_t += 1
    # predict_v = output[now_t][0].numpy()  # (6392,1) km/h

    # 计算变化前后各路段所需时间
    time1 = calculate_time(road_length, now_v)
    time_real = calculate_time(road_length, now_v)
    #time2 = calculate_time(road_length, predict_v)
    gol.set_value('time_before', time1)
    gol.set_value('time_after', time1)

    # closelist是全局的，避免走重复的路
    # gol.set_value('closeList', [])
    start_node = Node.Node(1570708754)
    end_node = Node.Node(1525870215)
    # gol.set_value('current node', start_node.data)
    a = A_star_contrast.A_star(start_node, end_node)
    path_time = 0

    if a.start():
        a.path()

    path_contrast = pd.read_pickle('./result/path_contrast.pkl')
    time_tmp = 0
    now_t += 1  # T1
    now_v = test['x'][now_t][0]
    time_real = calculate_time(road_length, now_v)
    for r in path_contrast:
        path_time += time_real[road_id_hash.get_index(r)][0]
        time_tmp += time_real[road_id_hash.get_index(r)][0]
        if time_tmp >= 0.25:
            now_t += 1  # T2
            now_v = test['x'][now_t][0]
            time_real = calculate_time(road_length, now_v)
            time_tmp = 0

    print('The path takes %f hours' % path_time)