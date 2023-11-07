import gol
import road_id_hash

# 描述A*算法中的结点数据(当前数据，父节点，步数）
class Node:
    def __init__(self, data, g=0, h=0):
        self.data = data
        self.index = road_id_hash.get_index(data)
        self.father = None  # 父节点
        self.g = g  # g值
        self.h = h  # h值

    # 启发函数（出发地和目的地之间的欧式距离除以当前路段速度）
    def setH(self, goal):
        velo = gol.get_value('velocity_now')
        dis = gol.get_value('road_dis')
        velo_now = velo[self.index][0]  # 单位km/h
        dis_to_goal = dis[self.index][goal.index]  # 单位m
        self.h = dis_to_goal*0.001 / velo_now

    # 实际代价（时间）
    def setG(self):
        time = gol.get_value('time_after')
        node = self
        while node.father is not None:
            self.g += time[self.index][1]
            node = node.father
        self.g += time[self.index][1]

    def setFather(self, node):
        self.father = node

    def getG(self):
        return self.g

    def getF(self):
        return self.g + self.h