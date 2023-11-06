import gol
import road_id_hash

# 描述A*算法中的结点数据(当前数据，父节点，步数）
class Node:
    def __init__(self, data, step=0, h=0):
        self.data = data
        self.index = road_id_hash.get_index(data)
        self.father = None  # 父节点
        self.g = step  # g值
        self.h = h  # h值

    # 启发函数（出发地和目的地之间的距离）
    def setH(self, goal):
        dis = gol.get_value('road_dis')
        self.h = dis[self.index][goal.index]

    # 实际代价（时间）
    def setG(self, find_ways):
        time = gol.get_value('time_after')
        for i in find_ways:
            self.g += time[i.index][1]
        self.g += time[self.index][1]

    def setFather(self, node):
        self.father = node

    def getG(self):
        return self.g

    def getF(self):
        return self.g + self.h