import pandas as pd
import numpy as np
import pickle
import folium
import networkx as nx
from road_id_hash import *
import random


def road_network_visual(df, adj_matrix, sub_road):
    # 创建Folium地图对象
    m = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=12)

    # 创建道路网络图
    G = nx.DiGraph()

    # 添加节点到图中
    for index, row in df.iterrows():
        G.add_node(row['link_id'], pos=(row['latitude'], row['longitude']))

    # 添加边到图中
    for i in range(len(adj_matrix)):
        for j in range(len(adj_matrix[i])):
            if adj_matrix[i][j] == 1:
                G.add_edge(sub_road[i], sub_road[j])

    # 遍历强连通分量
    for component in nx.strongly_connected_components(G):
        component_graph = G.subgraph(component)
        component_edges = list(component_graph.edges())

        # 创建GPS坐标点列表，连接起点和终点坐标
        connected_points = [
            [[df[df['link_id'] == edge[0]]['latitude'].values[0], df[df['link_id'] == edge[0]]['longitude'].values[0]],
             [df[df['link_id'] == edge[1]]['latitude'].values[0], df[df['link_id'] == edge[1]]['longitude'].values[0]]]
            for edge in component_edges]
        # print(connected_points)

        # 在地图上添加连接的道路形状
        for points in connected_points:
            folium.PolyLine(points, color="blue").add_to(m)

    # 保存地图为HTML文件
    m.save('./result/connected_roads_map.html')
    return m


# 路径轨迹可视化
def path_visual(df, path):
    m = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=12)
    colors = ['red', 'darkgreen', 'gray', 'purple', 'black']

    # 1. 对照组路线（不需要就直接注释掉）
    contrast_path = pd.read_pickle('result/path_contrast.pkl')

    start_gps = df[df['link_id'] == contrast_path[0]]
    end_gps = df[df['link_id'] == contrast_path[-1]]
    start_latitude = start_gps['latitude'].iloc[0]
    start_longitude = start_gps['longitude'].iloc[0]
    end_latitude = end_gps['latitude'].iloc[0]
    end_longitude = end_gps['longitude'].iloc[0]

    folium.Marker([start_latitude, start_longitude], tooltip=start_gps['link_id'].iloc[0]).add_to(m)
    folium.Marker([end_latitude, end_longitude], tooltip=end_gps['link_id'].iloc[0]).add_to(m)

    for i in range(len(contrast_path) - 1):
        start_link_id = contrast_path[i]
        end_link_id = contrast_path[i + 1]

        # 找到起点和终点的GPS坐标
        start_point = df[df['link_id'] == start_link_id]
        end_point = df[df['link_id'] == end_link_id]

        if not start_point.empty and not end_point.empty:
            # 创建GPS坐标点列表，连接起点和终点坐标
            points = [[start_point['latitude'].values[0], start_point['longitude'].values[0]],
                      [end_point['latitude'].values[0], end_point['longitude'].values[0]]]

            # 在地图上添加连接的路径
            folium.PolyLine(points, color="blue").add_to(m)

    # 多次动态规划路线（分段不同颜色显示）
    f = open(path, "rb")
    while 1:
        try:
            p = pickle.load(f)
            color = random.choice(colors)
            for i in range(len(p) - 1):
                start_link_id = p[i]
                end_link_id = p[i + 1]

                # 找到起点和终点的GPS坐标
                start_point = df[df['link_id'] == start_link_id]
                end_point = df[df['link_id'] == end_link_id]

                if not start_point.empty and not end_point.empty:
                    # 创建GPS坐标点列表，连接起点和终点坐标
                    points = [[start_point['latitude'].values[0], start_point['longitude'].values[0]],
                              [end_point['latitude'].values[0], end_point['longitude'].values[0]]]

                    # 在地图上添加连接的路径
                    folium.PolyLine(points, color=color).add_to(m)
        except EOFError:
            break

    m.save('./result/path.html')


# 路径点可视化（仅点）
def road_point_visual(df):
    # 创建一个Folium地图对象
    m = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=10)

    # 在地图上添加GPS坐标点标记
    for index, row in df.iterrows():
        folium.Marker([row['latitude'], row['longitude']], tooltip=row['link_id']).add_to(m)

    return m


# 路径规划的n次结果，link点可视化
def path_point_visual(sub_gps, m):
    colors = ['lightred', 'darkgreen', 'gray', 'beige', 'white', 'purple', 'black']
    f = open('./result/path.pkl', "rb")
    while 1:
        try:
            p = pickle.load(f)
            color = random.choice(colors)
            df = sub_gps[sub_gps['link_id'].isin(p)]
            for index, row in df.iterrows():
                folium.Marker([row['latitude'], row['longitude']], tooltip=row['link_id'],
                              icon=folium.Icon(color=color)).add_to(m)
        except EOFError:
            break

    m.save('./result/point_path.html')


if __name__ == '__main__':
    # 从 link_gps.v2 文件中读取路径点gps坐标
    file_path = "./data_use/link_gps_transformed.v2"
    data = pd.read_csv(file_path, header=None, delimiter='\t', names=['link_id', 'longitude', 'latitude'])  # (45148, 3)
    # 过滤出需要的路径点
    sub_road = pd.read_pickle('./data_use/road_network_linkid_filtered_6392.pkl')
    sub_gps = data[data['link_id'].isin(sub_road)]

    # 获取邻接矩阵
    # adj_matrix = pd.read_pickle('./data_use/adj_matrix_filtered_6392.pkl')
    # 子路网可视化
    # m = road_network_visual(sub_gps, adj_matrix, sub_road)
    # m.save('./result/road_network_6392.html')

    # 路径轨迹
    path = 'result/path.pkl'
    path_visual(sub_gps, path)

    # 只看轨迹点
    # contrast_path = pd.read_pickle('result/path_contrast.pkl')
    # contrast_path = sub_gps[sub_gps['link_id'].isin(contrast_path)]
    # m = road_point_visual(contrast_path)
    # path_point_visual(sub_gps, m)

