import pandas as pd
import math

import gol


# 定义计算Haversine距离的函数
def haversine(lon1, lat1, lon2, lat2):
    R = 6371  # 地球半径（单位：千米）
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance


def link_id_match(current_lon, current_lat):
    link_gps = gol.get_value('link_gps')
    # 初始化最小距离和最近的道路段的link_id
    min_distance = float('inf')
    nearest_link_id = None
    distance_threshold = 0.1  # 100m

    # 遍历道路数据集，找到最近的道路段
    for index, row in link_gps.iterrows():
        road_longitude = row['longitude']
        road_latitude = row['latitude']
        distance = haversine(current_lon, current_lat, road_longitude, road_latitude)
        if distance < min_distance:
            min_distance = distance
            nearest_link_id = row['link_id']

    if min_distance > distance_threshold:
        print("坐标超出地图范围")
        nearest_link_id = None

    return nearest_link_id


if __name__ == "__main__":
    file_path = "./data_use/link_gps_transformed.v2"
    data = pd.read_csv(file_path, header=None, delimiter='\t', names=['link_id', 'longitude', 'latitude'])
    sub_road = pd.read_pickle('./data_use/road_network_linkid_filtered_6392.pkl')
    link_gps = data[data['link_id'].isin(sub_road)]

    gol._init()
    gol.set_value('link_gps', link_gps)

    # 当前GPS坐标
    current_longitude = 116.42786
    current_latitude = 39.944906

    # 导航目标位置GPS坐标 (思考的方向，可以结合行驶的速度以及目的地来判断路段id)
    target_longitude = 116.20447774541552
    target_latitude = 39.90645159657411

    link_id = link_id_match(current_longitude, current_latitude)
    print(link_id)

