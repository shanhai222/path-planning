import pandas as pd
import numpy as np
import re
import pickle

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

#计算路段当下所需时间
def calculate_time(length, velocity):
    road_time = np.zeros((1448, 2))
    for i in range(0, 1448):
        road_time[i][0] = length[i][0]
        road_time[i][1] = length[i][1] / velocity[i][1]

    return road_time

if __name__ == '__main__':
    matrix = pd.read_pickle('./data_use/adj_matrix.pkl')
    length = pd.read_pickle('./data_use/road_filtered_length.pkl')
    road_id = pd.read_pickle('./data_use/road_linkid.pkl')
    #print(length.shape)
    #print(road_id)

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

    time1 = calculate_time(length, velocity1)
    time2 = calculate_time(length, velocity2)
    print(time1)