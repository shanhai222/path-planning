import pickle
import pandas as pd
import numpy as np
import torch
import gol
import A_star
import Node
import road_id_hash
from link_match import link_id_match

#计算路段当下所需时间(h)
def calculate_time(length, velocity):
    road_time = np.zeros((6392, 1))
    for i in range(0, 6392):
        # road_time[i][0] = length[i].values[0] / velocity[i]
        road_time[i][0] = length[i] / velocity[i]

    return road_time


if __name__ == '__main__':
    gol._init()
    # 路段信息读取
    adj_matrix = pd.read_pickle('./data_use/adj_matrix_filtered_6392.pkl')  # 路段间的邻接矩阵（有向）
    road_length = pd.read_pickle('./data_use/road_filtered_length_6392.pkl')  # 每个路段的长度
    #print(road_length[0])
    road_id = pd.read_pickle('./data_use/road_network_linkid_filtered_6392.pkl')  # 路段对应的id
    road_dis = pd.read_pickle('./data_use/dis_mat_6392.pkl')  # 路段间的直线距离
    link_gps = pd.read_csv('./data_use/link_gps_transformed.v2', header=None,
                           delimiter='\t', names=['link_id', 'longitude', 'latitude'])
    link_gps = link_gps[link_gps['link_id'].isin(road_id)]

    # 将路段id映射为index存储为字典
    road_id_mapping = road_id_hash.road_id_map(road_id)

    gol.set_value('adj_matrix', adj_matrix)
    gol.set_value('road_length', road_length)
    gol.set_value('road_id', road_id)
    gol.set_value('road_dis', road_dis)
    gol.set_value('link_gps', link_gps)
    gol.set_value('road_id_mapping', road_id_mapping)
    #print(length.shape)
    # print(road_id[1000])

    # 获取交通状况
    test = pd.read_pickle('./data_use/test_all.pkl')
    output = torch.load('./data_use/output_all.pth')  # 预测结果 (5795, 1, 6392, 1)
    #print(output.shape)
    # 随机取一个时间片作为出发时间
    # now_t = random.randint(0, 5795)
    now_t = 2990
    now_t_real = 2990  # T0
    # print(i)
    # 当前时间的实时路况
    now_v = test['x'][now_t][0]  # (6392,1)
    time_real = calculate_time(road_length, now_v)
    #print(now_v)
    gol.set_value('velocity_now', now_v)
    # 模型预测的下一个时间片的路况
    now_t += 1  # T1'
    predict_v = output[now_t][0].numpy()  # (6392,1) km/h

    # 计算变化前后各路段所需时间
    time1 = calculate_time(road_length, now_v)
    time2 = calculate_time(road_length, predict_v)
    gol.set_value('time_before', time1)
    gol.set_value('time_after', time2)

    # closelist是全局的，避免走重复的路
    gol.set_value('closeList', [])
    start_lon = 116.374107
    start_lat = 39.996142
    end_lon = 116.475587
    end_lat = 39.915614
    start_id = link_id_match(start_lon, start_lat)
    # start_id = 1570708754
    end_id = link_id_match(end_lon, end_lat)
    # end_id = 1525870215
    start_node = Node.Node(start_id)
    end_node = Node.Node(end_id)
    # gol.set_value('current node', start_node.data)
    a = A_star.A_star(start_node, end_node)
    path_time = 0


    while a.start():
        a.path()
        gol.set_value('closeList', a.next_close_list())
        replanning_road = a.find_15_minute()  # node
        #path_time += replanning_road.g
        if replanning_road.data == end_id:
            break
        start_node = Node.Node(replanning_road.data)
        end_node = Node.Node(end_id)
        now_t += int(replanning_road.g / 0.25)  # 当前路段所处的时间片 T2'
        now_v = test['x'][now_t][0]  # 当前的实时速度
        predict_v = output[now_t][0].numpy()  # 当前预测出的速度
        time1 = calculate_time(road_length, now_v)
        time2 = calculate_time(road_length, predict_v)
        gol.set_value('time_before', time1)
        gol.set_value('time_after', time2)
        a = A_star.A_star(start_node, end_node)

    f = open('./result/path.pkl', "rb")
    while 1:
        try:
            path = pickle.load(f)
            time_tmp = 0
            now_t_real += 1  # T1
            now_v = test['x'][now_t_real][0]
            time_real = calculate_time(road_length, now_v)
            for r in path:
                path_time += time_real[road_id_hash.get_index(r)][0]
                time_tmp += time_real[road_id_hash.get_index(r)][0]
                if time_tmp >= 0.25:
                    path = pickle.load(f)
                    now_t_real += 1  # T2
                    now_v = test['x'][now_t_real][0]
                    time_real = calculate_time(road_length, now_v)
                    time_tmp = 0
        except EOFError:
            break

    print('The path takes %f hours' % path_time)
